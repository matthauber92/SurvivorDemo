import unreal
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for a in actors.get_all_level_actors():
    if isinstance(a,unreal.DirectionalLight):
        print('LIGHT',a.get_actor_rotation(),a.light_component.get_editor_property('intensity'))
        a.set_actor_rotation(unreal.Rotator(pitch=-45,yaw=30,roll=0),False)
        a.light_component.set_editor_property('mobility',unreal.ComponentMobility.MOVABLE)
        a.light_component.set_editor_property('intensity',10.0)
    if isinstance(a,unreal.SkyLight):
        a.light_component.set_editor_property('mobility',unreal.ComponentMobility.MOVABLE)
        a.light_component.set_editor_property('real_time_capture',False)
        a.light_component.set_editor_property('intensity',1.0)
        a.light_component.recapture_sky()
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
