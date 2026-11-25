import unreal
import json
import traceback
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools

root = Path(unreal.Paths.project_dir()).resolve()
assert root.name == 'AIExample'
out = root / 'Saved/GASPValidation'
out.mkdir(parents=True, exist_ok=True)
result = {'completed': False, 'compiled': [], 'errors': []}
try:
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    registry.scan_paths_synchronous(['/Game'], True)
    # Use this pawn's owning controller for both camera systems; never player 0.
    base = unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC')
    graph = BlueprintTools.get_graph(base, 'SetupCamera')
    infos = [BlueprintTools._get_node_info(n) for n in BlueprintTools.find_nodes(graph)]
    cast = next(i for i in infos if i.type_id.endswith('CastToPlayerController'))
    controller_pin = next(p.pin_id for p in cast.output_pins if 'PlayerController' in p.type_id.replace(' ', ''))
    replaced = 0
    for info in infos:
        if info.type_id == 'Game|GetPlayerController':
            for pin in info.output_pins:
                for target in list(pin.connected_pins):
                    BlueprintTools.break_pins(pin.pin_id, target)
                    BlueprintTools.connect_pins(controller_pin, target)
            BlueprintTools.delete_node(info.node)
            replaced += 1
    result['camera_player_zero_nodes_replaced'] = replaced
    BlueprintTools.compile_blueprint(base)
    unreal.EditorAssetLibrary.save_loaded_asset(base)
    character = unreal.load_asset('/Game/AIExample/Gameplay/Characters/BP_SurvivorCharacter')
    gm_path = '/Game/AIExample/Gameplay/BP_SurvivorGameMode'
    assert not unreal.EditorAssetLibrary.does_asset_exist(gm_path), 'Refusing to overwrite GameMode'
    factory = unreal.BlueprintFactory()
    factory.set_editor_property('parent_class', unreal.GameModeBase)
    gm = unreal.AssetToolsHelpers.get_asset_tools().create_asset('BP_SurvivorGameMode', '/Game/AIExample/Gameplay', unreal.Blueprint, factory)
    BlueprintTools.compile_blueprint(gm)
    gm_cdo = unreal.get_default_object(gm.generated_class())
    gm_cdo.set_editor_property('default_pawn_class', character.generated_class())
    gm_cdo.set_editor_property('player_controller_class', unreal.PlayerController)
    BlueprintTools.compile_blueprint(gm)
    assert unreal.EditorAssetLibrary.save_loaded_asset(gm)
    level_path = '/Game/AIExample/Maps/Lvl_CharacterTest'
    assert not unreal.EditorAssetLibrary.does_asset_exist(level_path), 'Refusing to overwrite test level'
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    assert level_subsystem.new_level(level_path)
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    world.get_world_settings().set_editor_property('default_game_mode', gm.generated_class())
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    cube = unreal.load_asset('/Engine/BasicShapes/Cube')
    material = unreal.load_asset('/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray')
    def block(name, location, scale, rotation=unreal.Rotator()):
        actor = actors.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(*location), rotation)
        actor.set_actor_label(name)
        actor.static_mesh_component.set_static_mesh(cube)
        actor.static_mesh_component.set_material(0, material)
        actor.static_mesh_component.set_collision_profile_name('BlockAll')
        actor.set_actor_scale3d(unreal.Vector(*scale))
        return actor
    block('Locomotion Test Floor', (0,0,-50), (200,200,1))
    block('Collision Test Wall', (2500,0,150), (1,30,3))
    block('Camera Collision Wall', (-700,800,150), (1,20,3))
    block('Slope Test Ramp', (0,1800,125), (10,5,0.5), unreal.Rotator(15,0,0))
    for i in range(14):
        start = actors.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(-1200 + (i%7)*180, -1200+(i//7)*200, 110))
        start.set_actor_label('Survivor PlayerStart %02d' % (i+1))
    sun = actors.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0,0,2000), unreal.Rotator(-45,-30,0))
    sun.light_component.set_editor_property('intensity', 5.0)
    actors.spawn_actor_from_class(unreal.SkyAtmosphere, unreal.Vector(0,0,0))
    sky = actors.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0,0,1000))
    sky.light_component.set_editor_property('real_time_capture', True)
    assert level_subsystem.save_current_level()
    report = root/'MigrationStaging/GASP-20261117-054307/dependency-report.json'
    if not report.is_file():
        report = root.parent/'AIExample-Archive/DirectoryCleanup-20261124/Migrations/GASP-20261117-054307/dependency-report.json'
    manifest = json.loads(report.read_text())
    packages = manifest['packages'] + [gm_path]
    for package in packages:
        data = registry.get_assets_by_package_name(package)
        if not data or str(data[0].asset_class_path.asset_name) not in ('Blueprint','AnimBlueprint'):
            continue
        try:
            bp = unreal.load_asset(package)
            BlueprintTools.compile_blueprint(bp)
            assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
            result['compiled'].append(package)
        except Exception as exc:
            result['errors'].append({'package':package,'error':str(exc)})
    result['completed'] = not result['errors']
    result['level'] = level_path
    unreal.EditorLevelLibrary.set_level_viewport_camera_info(unreal.Vector(-1800,-2200,900), unreal.Rotator(-18,40,0))
except Exception:
    result['errors'].append(traceback.format_exc())
finally:
    (out/'setup-result.json').write_text(json.dumps(result,indent=2))
    unreal.log('AIEXAMPLE_SETUP_RESULT ' + json.dumps(result))
