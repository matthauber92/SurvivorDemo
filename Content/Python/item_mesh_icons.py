"""Bake selected item definitions or static meshes into transparent UI textures."""
import binascii
import math
import struct
import zlib
from pathlib import Path

import unreal as u


def png_chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", binascii.crc32(kind + data))


def render(mesh, path, width=256, height=256, parts=()):
    vertices, faces = [], []
    for part, socket in [(mesh, None), *parts]:
        for section in range(part.get_num_sections(0)):
            points, indices, *_ = u.ProceduralMeshLibrary.get_section_from_static_mesh(part, 0, section)
            base = len(vertices)
            if socket:
                rotation = socket.relative_rotation.quaternion()
                points = [rotation.rotate_vector(p * socket.relative_scale) + socket.relative_location for p in points]
            vertices.extend((p.x, p.y, p.z) for p in points)
            faces.extend(tuple(base + indices[i+j] for j in range(3)) for i in range(0, len(indices), 3))
    if not faces:
        raise ValueError(f"{mesh.get_name()} has no render triangles")
    # Rotate the mesh's long horizontal axis onto the canvas, then reveal the top and end.
    box = mesh.get_bounding_box()
    extent = box.max - box.min
    projected = []
    for x, y, z in vertices:
        if extent.y > extent.x:
            x, y = y, -x
        side = .985*x + .174*y
        depth = -.174*x + .985*y
        projected.append((side, .966*z + .259*depth, .966*depth - .259*z))
    xs, ys, _ = zip(*projected)
    scale = .91 * min(width / max(max(xs)-min(xs), .001), height / max(max(ys)-min(ys), .001))
    cx, cy = (max(xs)+min(xs))/2, (max(ys)+min(ys))/2
    projected = [((x-cx)*scale+width/2, (cy-y)*scale+height/2, d*scale) for x,y,d in projected]
    pixels = bytearray(width*height*4)
    depths = [math.inf]*(width*height)
    for a,b,c in faces:
        x,y,z = projected[a]
        bx,by,bz = projected[b]
        cx,cy,cz = projected[c]
        dx,dy,dz = bx-x,by-y,bz-z
        ex,ey,ez = cx-x,cy-y,cz-z
        area = dx*ey-dy*ex
        if abs(area)<.00001:
            continue
        nx,ny = dy*ez-dz*ey, dz*ex-dx*ez
        length = math.sqrt(nx*nx+ny*ny+area*area)
        light = max(0, (nx*.32+ny*.70+area*.63)*math.copysign(1,area)/length)
        value = int(122+122*light)
        color = bytes((value,min(255,value+5),min(255,value+8),255))
        for row in range(max(0,math.floor(min(y,by,cy))),min(height,math.ceil(max(y,by,cy)))):
            for col in range(max(0,math.floor(min(x,bx,cx))),min(width,math.ceil(max(x,bx,cx)))):
                px,py = col+.5-x,row+.5-y
                s,t = (px*ey-py*ex)/area,(dx*py-dy*px)/area
                if s<0 or t<0 or s+t>1:
                    continue
                depth = z+s*dz+t*ez
                i = row*width+col
                if depth<depths[i]:
                    depths[i] = depth
                    pixels[4*i:4*i+4] = color
    rows = b"".join(b"\0"+pixels[i:i+4*width] for i in range(0,len(pixels),4*width))
    path.write_bytes(b"\x89PNG\r\n\x1a\n"+png_chunk(b"IHDR",struct.pack(">IIBBBBB",width,height,8,6,0,0,0))+png_chunk(b"IDAT",zlib.compress(rows))+png_chunk(b"IEND",b""))


def capture_item(mesh, path, width, height, parts=(), fill=.70):
    actors = u.get_editor_subsystem(u.EditorActorSubsystem)
    world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    origin = u.Vector(0, 0, 50000)
    spawned = []

    def spawn(cls, position, rotation):
        actor = actors.spawn_actor_from_class(cls, position, rotation, transient=True)
        spawned.append(actor)
        return actor

    try:
        body = spawn(u.StaticMeshActor, origin, u.Rotator())
        component = body.static_mesh_component
        component.set_mobility(u.ComponentMobility.MOVABLE)
        component.set_static_mesh(mesh)
        components = [component]
        for part, socket in parts:
            part_actor = spawn(u.StaticMeshActor, origin, u.Rotator())
            child = part_actor.static_mesh_component
            child.set_mobility(u.ComponentMobility.MOVABLE)
            child.set_static_mesh(part)
            snap = u.AttachmentRule.SNAP_TO_TARGET
            child.attach_to_component(component, socket.socket_name, snap, snap, snap, False)
            components.append(child)
        bounds = [c.get_owner().get_actor_bounds(False) for c in components]
        lo = [min(getattr(c, a)-getattr(e, a) for c,e in bounds) for a in "xyz"]
        hi = [max(getattr(c, a)+getattr(e, a) for c,e in bounds) for a in "xyz"]
        center = (u.Vector(*hi)+u.Vector(*lo))*.5
        extent = (u.Vector(*hi)-u.Vector(*lo))*.5
        yaw = 80 if extent.x >= extent.y else -10
        view = u.Rotator(roll=0, pitch=-16, yaw=yaw)
        camera = spawn(u.SceneCapture2D, center - view.get_forward_vector()*200, view)
        capture = camera.capture_component2d
        capture.set_editor_property('capture_every_frame', False)
        capture.set_editor_property('capture_on_movement', False)
        capture.set_editor_property('projection_type', u.CameraProjectionMode.ORTHOGRAPHIC)
        def span(axis):
            return 2*(abs(axis.x)*extent.x + abs(axis.y)*extent.y + abs(axis.z)*extent.z)
        capture.set_editor_property('ortho_width', max(span(view.get_right_vector()), span(view.get_up_vector())*width/height)/fill)
        capture.set_editor_property('primitive_render_mode', u.SceneCapturePrimitiveRenderMode.PRM_USE_SHOW_ONLY_LIST)
        for visible in components:
            capture.show_only_component(visible)
        capture.set_editor_property('capture_source', u.SceneCaptureSource.SCS_SCENE_COLOR_HDR)
        target = u.RenderingLibrary.create_render_target2d(world, width, height, u.TextureRenderTargetFormat.RTF_RGBA16F)
        capture.set_editor_property('texture_target', target)
        capture.capture_scene()
        colors = u.RenderingLibrary.read_render_target_raw(world, target, normalize=False)
        capture.set_editor_property('capture_source', u.SceneCaptureSource.SCS_BASE_COLOR)
        capture.capture_scene()
        albedo = u.RenderingLibrary.read_render_target_raw(world, target, normalize=False)
        capture.set_editor_property('capture_source', u.SceneCaptureSource.SCS_NORMAL)
        capture.capture_scene()
        normals = u.RenderingLibrary.read_render_target_raw(world, target, normalize=False)
        key = view.get_up_vector()*.76 - view.get_forward_vector()*.60 - view.get_right_vector()*.25
        rows = bytearray()
        for index, color in enumerate(colors):
            if index % width == 0:
                rows.append(0)
            alpha = max(0, min(1, 1-color.a))
            base = albedo[index]
            normal = normals[index]
            diffuse = max(0, min(1, normal.r*key.x + normal.g*key.y + normal.b*key.z))
            for value in (base.r, base.g, base.b):
                mapped = min(1, max(0, value)/max(alpha,.001)*(.85+.40*diffuse) + .025*diffuse)
                rows.append(round(255*(12.92*mapped if mapped <= .0031308 else 1.055*mapped**(1/2.4)-.055)))
            rows.append(round(255*alpha))
        path.write_bytes(b"\x89PNG\r\n\x1a\n"+png_chunk(b"IHDR",struct.pack(">IIBBBBB",width,height,8,6,0,0,0))+png_chunk(b"IDAT",zlib.compress(rows))+png_chunk(b"IEND",b""))
    finally:
        for actor in reversed(spawned):
            actors.destroy_actor(actor)


def generate(asset):
    item = isinstance(asset, u.DataAsset)
    mesh = asset.get_editor_property("WorldMesh") if item else asset
    if not isinstance(mesh,u.StaticMesh):
        raise ValueError("Choose an item definition with a WorldMesh or a static mesh")
    name = "T_Icon_"+asset.get_name().removeprefix("DA_")
    folder = Path(u.Paths.convert_relative_path_to_full(u.Paths.project_saved_dir()))/"ItemIcons"
    folder.mkdir(exist_ok=True)
    png = folder/(name+".png")
    parts = []
    width, height = 256, 256
    if item and str(asset.get_editor_property("Category")) in ("Weapon", "Attachment"):
        width, height = 384, 160
        socket = mesh.find_socket("Magazine")
        if socket:
            survivor = u.load_class(None, "/Game/Survivor/Interaction/BP_SurvivorInteractionCharacter.BP_SurvivorInteractionCharacter_C")
            magazine = u.get_default_object(survivor).call_method("DefaultMagazineMesh", (asset.get_editor_property("ItemID"),))
            if magazine:
                parts.append((magazine, socket))
    if item and str(asset.get_editor_property("Category")) in ("Weapon","Attachment","Ammo"):
        capture_item(mesh, png, width, height, parts, .70 if str(asset.get_editor_property("Category")) == "Attachment" else .94)
    else:
        render(mesh, png, width, height, parts)
    task = u.AssetImportTask()
    task.filename,task.destination_path = str(png),"/Game/Survivor/UI/Icons"
    task.automated,task.replace_existing,task.save = True,True,True
    u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    texture = u.load_asset(task.destination_path+"/"+name)
    texture.set_editor_property("lod_group",u.TextureGroup.TEXTUREGROUP_UI)
    texture.set_editor_property("compression_settings",u.TextureCompressionSettings.TC_EDITOR_ICON)
    u.EditorAssetLibrary.save_loaded_asset(texture,False)
    if item:
        asset.set_editor_property("InventoryIcon", texture)
        u.EditorAssetLibrary.save_loaded_asset(asset, False)
    return texture


def generate_selected():
    for asset in u.EditorUtilityLibrary.get_selected_assets():
        if isinstance(asset,u.StaticMesh) or (isinstance(asset,u.DataAsset) and asset.get_class().get_name()=="PDA_ItemDefinition_C"):
            generate(asset)

