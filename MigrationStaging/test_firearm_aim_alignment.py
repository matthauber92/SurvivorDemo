import unreal,time,json,traceback,math
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();inv=pc.get_editor_property('InventoryComponent');state={'weapon':0,'pitch':0,'phase':0,'next':time.monotonic()+.5};report={'samples':[]};R='/Game/AIExample/'
def finish():
 report['passed']='error' not in report and all(s['angle_error_deg']<20 for s in report['samples']);(Path(unreal.Paths.project_saved_dir())/'firearm-aim-result.json').write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(aim_alignment_handle)
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  name=['Revolver','Shotgun'][state['weapon']];slot=2 if name=='Revolver' else 0;pitch=[0,30,-30][state['pitch']]
  if state['phase']==0:
   if state['pitch']==0:
    assert inv.call_method('TryAddItem',(unreal.load_asset(R+'Items/DA_'+name+'Item'),1));ix=list(inv.get_editor_property('ItemIDs')).index(unreal.Name('Weapon.'+name));uid=inv.get_editor_property('BackpackInstances')[ix];state['uid']=uid
    assert inv.call_method('TryTransferWeapon',(list(inv.get_editor_property('SlotOrder')).index(ix),slot+8,uid,inv.get_editor_property('LayoutVersion')));assert inv.call_method('TrySelectWeapon',(slot,uid,inv.get_editor_property('LayoutVersion')))
   pc.set_control_rotation(unreal.Rotator(pitch=pitch));assert inv.call_method('TryPistolAction',(1,state['uid'],p.get_actor_location(),unreal.Vector(1,0,0)))
   state['phase']=1;state['next']=time.monotonic()+1.4
  else:
   v=p.call_method('GetActiveWeaponVisual');forward=unreal.MathLibrary.get_forward_vector(v.get_socket_rotation('Muzzle'));desired=unreal.MathLibrary.get_forward_vector(pc.get_control_rotation());dot=max(-1,min(1,forward.dot(desired)));report['samples'].append({'weapon':name,'pitch':pitch,'angle_error_deg':math.degrees(math.acos(dot)),'anim':p.mesh.get_anim_instance().get_class().get_path_name()})
   state['pitch']+=1
   if state['pitch']==3:state['pitch']=0;state['weapon']+=1
   if state['weapon']==2:finish();return
   state['phase']=0;state['next']=time.monotonic()+.1
 except Exception:report['error']=traceback.format_exc();finish()
aim_alignment_handle=unreal.register_slate_post_tick_callback(tick)
