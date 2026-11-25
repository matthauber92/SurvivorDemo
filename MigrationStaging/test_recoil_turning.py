import unreal,time,json,traceback,math
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();inv=pc.get_editor_property('InventoryComponent');report={'checks':{},'samples':[]};state={'phase':0,'next':time.monotonic()+.5}
def check(n,v):report['checks'][n]=bool(v);assert v,n
def angle(a,b):return (a-b+180)%360-180
def finish():
 report['passed']='error' not in report and all(report['checks'].values());(Path(unreal.Paths.project_saved_dir())/'recoil-turning-result.json').write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(recoil_test_handle)
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   check('add',inv.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_ShotgunItem'),1)))
   ix=list(inv.get_editor_property('ItemIDs')).index(unreal.Name('Weapon.Shotgun'));uid=inv.get_editor_property('BackpackInstances')[ix];state['uid']=uid
   check('equip',inv.call_method('TryTransferWeapon',(list(inv.get_editor_property('SlotOrder')).index(ix),8,uid,inv.get_editor_property('LayoutVersion'))));check('draw',inv.call_method('TrySelectWeapon',(0,uid,inv.get_editor_property('LayoutVersion'))))
   pc.set_control_rotation(unreal.Rotator());state['next']=time.monotonic()+1.5
  elif phase==1:
   before=p.get_actor_rotation().yaw;loc=p.get_actor_location();pc.set_control_rotation(unreal.Rotator(yaw=140));p.call_method('NoteHipFire')
   check('shot_does_not_snap_actor',abs(angle(p.get_actor_rotation().yaw,before))<.01);check('shot_does_not_move_actor',(p.get_actor_location()-loc).length()<.01)
   # Clear recent-shot state by waiting; check idle independently.
   state['next']=time.monotonic()+3.2
  elif phase==2:
   check('idle_body_follows_camera',abs(angle(p.get_actor_rotation().yaw,140))<5)
   state['yaw']=140;state['steps']=0;state['phase']=3;state['next']=time.monotonic();return
  elif phase==3:
   state['yaw']+=30;pc.set_control_rotation(unreal.Rotator(yaw=state['yaw']));state['steps']+=1
   report['samples'].append({'target':state['yaw']-30,'body':p.get_actor_rotation().yaw})
   if state['steps']<13:state['next']=time.monotonic()+.4;return
   check('idle_tracks_full_camera_orbit',all(abs(angle(s['body'],s['target']))<10 for s in report['samples']))
   pc.set_control_rotation(unreal.Rotator());state['next']=time.monotonic()+1.4
  elif phase==4:
   check('aim_walk',inv.call_method('TryPistolAction',(1,state['uid'],p.get_actor_location(),unreal.Vector(1,0,0))) and p.call_method('GetDesiredGait').value==0)
   check('fire',inv.call_method('TryPistolAction',(2,state['uid'],p.get_actor_location()+unreal.Vector(0,0,50),unreal.Vector(1,0,0))))
   state['initial_pending']=p.get_editor_property('RecoilPitchRemaining');check('camera_kick_queued',state['initial_pending']<-.5)
   check('eight_pellets',len(p.get_editor_property('PublicShotEnds'))==8)
   state['next']=time.monotonic()+.15
  elif phase==5:
   report['pending_after_150ms']=p.get_editor_property('RecoilPitchRemaining');check('recoil_decays',abs(report['pending_after_150ms'])<abs(state['initial_pending']))
   state['next']=time.monotonic()+1
  elif phase==6:
   check('recoil_settled',abs(p.get_editor_property('RecoilPitchRemaining'))<.01)
   v=p.call_method('GetActiveWeaponVisual');check('socket_preserved',str(v.get_attach_socket_name())=='ShotgunGrip_R' and v.get_editor_property('relative_location').length()<.01)
   finish();return
  state['phase']+=1
 except Exception:report['error']=traceback.format_exc();finish()
recoil_test_handle=unreal.register_slate_post_tick_callback(tick)
