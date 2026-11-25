import unreal,time,json,math,gc,types
from pathlib import Path
for obj in gc.get_objects():
 if isinstance(obj,types.FunctionType) and obj.__name__=='measure_aim_tick':
  state=obj.__globals__.get('aim_measure',{})
  if 'handle' in state:
   try:unreal.unregister_slate_post_tick_callback(state['handle'])
   except Exception:pass
aw=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];ap=unreal.GameplayStatics.get_player_pawn(aw,0);ac=ap.get_controller();ag=ap.get_editor_property('SidearmVisual')
aim_measure={'i':0,'next':time.monotonic()+.6,'rows':[]};angles=[-50,0,50];ac.set_control_rotation(unreal.Rotator(pitch=angles[0],yaw=0,roll=0))
def measure_aim_tick(dt):
 if time.monotonic()<aim_measure['next']:return
 angle=angles[aim_measure['i']];v=ag.get_forward_vector();r=unreal.MathLibrary.make_rot_from_x(v)
 aim_measure['rows'].append({'camera_pitch':angle,'gun_pitch':r.pitch,'gun_yaw':r.yaw,'gun_roll':ag.get_world_rotation().roll})
 aim_measure['i']+=1
 if aim_measure['i']==len(angles):
  unreal.unregister_slate_post_tick_callback(aim_measure['handle']);ac.set_control_rotation(unreal.Rotator());(Path(unreal.Paths.project_saved_dir())/'ShoulderCamera/aim-before.json').write_text(json.dumps(aim_measure['rows'],indent=2));return
 ac.set_control_rotation(unreal.Rotator(pitch=angles[aim_measure['i']],yaw=0,roll=0));aim_measure['next']=time.monotonic()+.6
aim_measure['handle']=unreal.register_slate_post_tick_callback(measure_aim_tick)
