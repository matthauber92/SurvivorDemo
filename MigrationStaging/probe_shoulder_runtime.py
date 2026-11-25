import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();cm=unreal.GameplayStatics.get_player_camera_manager(w,0)
print('CAMERA',cm.get_camera_location(),cm.get_fov_angle(),p.get_actor_location())
for c in p.get_components_by_class(unreal.SceneComponent):
 if isinstance(c,(unreal.CameraComponent,unreal.SpringArmComponent)):
  print(c.get_name(),'active',c.is_active(),'location',c.get_world_location(),'parent',c.get_attach_parent(), 'arm',c.get_editor_property('target_arm_length') if isinstance(c,unreal.SpringArmComponent) else c.get_editor_property('field_of_view'))
print('DEFAULTS',[(n,p.get_editor_property(n)) for n in ['CameraWalkDistance','CameraSprintDistance','CameraAimDistance','ShouldShowCrosshair']])
unreal.SystemLibrary.execute_console_command(w,'Shot',pc)
