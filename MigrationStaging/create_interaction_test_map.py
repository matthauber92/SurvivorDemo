import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
def run():
    root='/Game/AIExample/Interaction'
    report={}
    for name in ['BPI_Interactable','BP_InteractionComponent','BP_InteractionTestDoor','BP_SurvivorInteractionCharacter','BP_InteractionHUD','BP_InteractionTestGameMode']:
        bp=unreal.load_asset(root+'/'+name)
        B.compile_blueprint(bp)
        report[name]=str(bp.get_editor_property('status'))
    level='/Game/AIExample/Maps/Lvl_InteractionTest'
    ls=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if unreal.EditorAssetLibrary.does_asset_exist(level):assert ls.load_level(level)
    else:assert ls.new_level(level)
    world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    world.get_world_settings().set_editor_property('default_game_mode',unreal.load_asset(root+'/BP_InteractionTestGameMode').generated_class())
    actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    floor=actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(0,0,-50))
    floor.set_actor_label('Interaction Test Floor')
    floor.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'))
    floor.static_mesh_component.set_material(0,unreal.load_asset('/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray'))
    floor.static_mesh_component.set_collision_profile_name('BlockAll')
    floor.set_actor_scale3d(unreal.Vector(60,60,1))
    for i in range(14):
        start=actors.spawn_actor_from_class(unreal.PlayerStart,unreal.Vector(-180-i//2*180,-90+(i%2)*180,100))
        start.set_actor_label('Interaction PlayerStart %02d'%(i+1))
    door=actors.spawn_actor_from_class(unreal.load_asset(root+'/BP_InteractionTestDoor').generated_class(),unreal.Vector(0,-60,0))
    door.set_actor_label('Interaction Test Door')
    actors.spawn_actor_from_class(unreal.DirectionalLight,unreal.Vector(0,0,1000),unreal.Rotator(pitch=-45,yaw=30,roll=0))
    actors.spawn_actor_from_class(unreal.SkyAtmosphere,unreal.Vector())
    sky=actors.spawn_actor_from_class(unreal.SkyLight,unreal.Vector(0,0,500));sky.light_component.set_editor_property('real_time_capture',False)
    assert ls.save_current_level()
    (Path(unreal.Paths.project_saved_dir())/'InteractionValidation/compile-result.json').write_text(json.dumps(report,indent=2))
    print(report)
run()

