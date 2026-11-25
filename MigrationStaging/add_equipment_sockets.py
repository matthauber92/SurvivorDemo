import unreal,toolset_registry,shutil,json
from pathlib import Path
from datetime import datetime
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.skeletal_mesh import SkeletalMeshTools as S
root=Path(unreal.Paths.project_dir());out=Path(unreal.Paths.project_saved_dir())/'EquipmentSocketValidation';out.mkdir(exist_ok=True)
backup=root/'Backups'/('BeforeEquipmentSockets-'+datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir(parents=True)
for path in ['AIExample/Interaction/BP_SurvivorInteractionCharacter.uasset','Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin.uasset']:
 dst=backup/path;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/'Content'/path,dst)
mesh=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin')
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter')
specs=[
 ('PistolGrip_R','hand_r',(-13,2,3),(0,180,0)),
 ('PistolHolster','pelvis',(-5,-2,19.5),(0,170,-90)),
 ('LongGunGrip_R','hand_r',(-4,0,5),(0,180,0)),
 ('PrimaryHolster','spine_03',(10,-18,-12),(0,0,0)),
 ('SecondaryHolster','spine_03',(10,-18,12),(0,0,0)),
]
with toolset_registry.tool_raising_exceptions():
 for name,bone,location,rotation in specs:
  # Preserve future manual socket edits if this migration is run again.
  if mesh.find_socket(name):continue
  socket=S.add_socket(mesh,name,bone)
  socket.set_editor_property('relative_location',unreal.Vector(*location))
  socket.set_editor_property('relative_rotation',unreal.Rotator(pitch=rotation[0],yaw=rotation[1],roll=rotation[2]))
  socket.set_editor_property('relative_scale',unreal.Vector(1,1,1))
 assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
 B.write_graph_dsl(B.get_graph(bp,'UpdateWeaponVisual'),'''(fn UpdateWeaponVisual (Slot ID Visual)
 (Development|SetHiddeninGame :self Visual :NewHidden true)
 (if (or (== ID "Weapon.Pistol") (== ID "Weapon.TestLongGun"))
  (if (== ID "Weapon.Pistol")
   (Components|StaticMesh|SetStaticMesh :self Visual :NewMesh "/Game/AIExample/Weapons/TheHouse/04_Weapons/Pistol/Mesh/SM_Pistol.SM_Pistol")
   (else (Components|StaticMesh|SetStaticMesh :self Visual :NewMesh "/Engine/BasicShapes/Cube.Cube")))
  (Variables|Default|SetAttachSocket "PrimaryHolster")
  (if (== Slot 1) (Variables|Default|SetAttachSocket "SecondaryHolster"))
  (if (== Slot 2) (Variables|Default|SetAttachSocket "PistolHolster"))
  (if (== Slot (Variables|Default|GetPublicActiveSlot))
   (if (== ID "Weapon.Pistol")
    (Variables|Default|SetAttachSocket "PistolGrip_R")
    (else (Variables|Default|SetAttachSocket "LongGunGrip_R"))))
  (Transformation|AttachComponentToComponent :self Visual :Parent (Variables|Character|GetMesh) :SocketName (Variables|Default|GetAttachSocket) :LocationRule "SnapToTarget" :RotationRule "SnapToTarget" :ScaleRule "SnapToTarget" :bWeldSimulatedBodies false)
  (if (== ID "Weapon.TestLongGun")
   (Transformation|SetRelativeScale3D :self Visual :NewScale3D "0.65,0.07,0.12")
   (else (Transformation|SetRelativeScale3D :self Visual :NewScale3D "1,1,1")))
  (Development|SetHiddeninGame :self Visual :NewHidden false)))''')
 B.compile_blueprint(bp,warnings_as_errors=True)
 assert bp.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE
 assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 code=B.read_graph_dsl(B.get_graph(bp,'UpdateWeaponVisual'))
 assert 'SetRelativeTransform' not in code and 'SetRelativeLocation' not in code and 'SetRelativeRotation' not in code
 (out/'migration.json').write_text(json.dumps({'mesh':mesh.get_path_name(),'sockets':[{'name':n,'bone':b,'transform':S.get_socket_transform(mesh,n).export_text()} for n,b,_,_ in specs],'backup':str(backup),'graph':code},indent=2))
 print('EQUIPMENT_SOCKETS_SAVED',S.get_socket_names(mesh))
