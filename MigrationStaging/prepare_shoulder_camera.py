import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
from editor_toolset.toolsets.actor import ActorTools as A
bp=asset('Interaction/BP_SurvivorInteractionCharacter')
with toolset_registry.tool_raising_exceptions():
 comps=A.get_components(B.get_default_object(bp))
 boom=next((c for c in comps if c.get_name()=='ShoulderBoom_GEN_VARIABLE'),None)
 if not boom:boom=A.add_component(bp,unreal.SpringArmComponent.static_class(),'ShoulderBoom')
 for k,v in {'target_arm_length':350.0,'socket_offset':unreal.Vector(0,65,45),'use_pawn_control_rotation':True,'do_collision_test':True,'probe_size':12.0,'probe_channel':unreal.CollisionChannel.ECC_CAMERA,'enable_camera_lag':True,'camera_lag_speed':12.0,'camera_lag_max_distance':35.0,'enable_camera_rotation_lag':False,'use_camera_lag_substepping':True}.items():boom.set_editor_property(k,v)
 cam=next((c for c in A.get_components(B.get_default_object(bp)) if c.get_name()=='ShoulderCamera_GEN_VARIABLE'),None)
 if not cam:cam=A.add_component(boom,unreal.CameraComponent.static_class(),'ShoulderCamera')
 cam.set_editor_property('field_of_view',70.0);cam.set_editor_property('use_pawn_control_rotation',False);cam.set_editor_property('auto_activate',False)
 for name,default in [('CameraWalkDistance',350.0),('CameraSprintDistance',600.0),('CameraAimDistance',220.0),('CameraWalkFOV',70.0),('CameraSprintFOV',76.0),('CameraAimFOV',60.0),('CameraBlendSpeed',5.0),('CameraAimBlendSpeed',10.0)]:
  var(bp,name,'float')
 B.compile_blueprint(bp,warnings_as_errors=True)
 for name,default in [('CameraWalkDistance',350.0),('CameraSprintDistance',600.0),('CameraAimDistance',220.0),('CameraWalkFOV',70.0),('CameraSprintFOV',76.0),('CameraAimFOV',60.0),('CameraBlendSpeed',5.0),('CameraAimBlendSpeed',10.0)]:B.get_default_object(bp).set_editor_property(name,default)
 var(bp,'ShoulderCameraAiming','bool')
 fn(bp,'UpdateShoulderCamera',[('DeltaSeconds','float')]);fn(bp,'InitializeShoulderCamera')
 B.compile_blueprint(bp,warnings_as_errors=True)
 g=B.get_graph(bp,'UpdateShoulderCamera')
 for search in ['*TargetArmLength*','*SocketOffset*','*FieldOfView*','*InterpTo*','*Deactivate*','*GetGait*','*GetShoulder*']:
  print(search,B.find_node_types(g,search.strip('*')))
