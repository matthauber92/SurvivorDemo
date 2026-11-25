import unreal,time,json
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);a=p.mesh.get_anim_instance();obs={'samples':[]};end=time.monotonic()+5
p.get_controller().set_control_rotation(unreal.Rotator(yaw=140))
def observe(dt):
 root=p.mesh.get_socket_rotation('root');component=p.mesh.get_world_rotation()
 obs['samples'].append({'root_yaw':root.yaw,'mesh_yaw':component.yaw,'turn_in_place':a.call_method('ShouldTurnInPlace')})
 if time.monotonic()>end:
  (Path(unreal.Paths.project_saved_dir())/'armed-turn-observation.json').write_text(json.dumps(obs,indent=2));unreal.unregister_slate_post_tick_callback(turn_observer)
turn_observer=unreal.register_slate_post_tick_callback(observe)
