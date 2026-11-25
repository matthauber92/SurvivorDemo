import unreal,json,time,traceback
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();inv=pc.get_editor_property('InventoryComponent')
R='/Game/AIExample/';report={'checks':{}};state={'phase':0,'next':time.monotonic()+.3,'weapon':0};out=Path(unreal.Paths.project_saved_dir())/'extra-firearms-result.json'
def check(n,v):report['checks'][n]=bool(v);assert v,n
def prop(o,n):return o.get_editor_property(n)
def action(n):
 origin=p.get_actor_location()+unreal.Vector(0,0,50);direction=unreal.Vector(1,0,0)
 pc.set_control_rotation(unreal.Rotator())
 return inv.call_method('TryPistolAction',(n,state['uid'],origin,direction))
def finish():
 report['passed']='error' not in report and all(report['checks'].values());out.write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(extra_firearms_handle)
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  name=['Revolver','Shotgun'][state['weapon']];slot=2 if name=='Revolver' else 0;phase=state['phase'];capacity=6 if name=='Revolver' else 2
  if phase==0:
   check(name+'_add',inv.call_method('TryAddItem',(unreal.load_asset(R+'Items/DA_'+name+'Item'),1)))
   check(name+'_ammo_add',inv.call_method('TryAddItem',(unreal.load_asset(R+'Items/DA_'+name+'Ammo'),24)))
   ids=list(prop(inv,'ItemIDs'));index=ids.index(unreal.Name('Weapon.'+name));uid=prop(inv,'BackpackInstances')[index];state['uid']=uid
   check(name+'_equip',inv.call_method('TryTransferWeapon',(list(prop(inv,'SlotOrder')).index(index),8+slot,uid,prop(inv,'LayoutVersion'))))
   check(name+'_draw',inv.call_method('TrySelectWeapon',(slot,uid,prop(inv,'LayoutVersion'))))
   state['index']=inv.call_method('GetActivePistolIndex');check(name+'_active_index',state['index']>=0)
   p.set_actor_location(unreal.Vector(0,0,1200),False,True);p.character_movement.set_movement_mode(unreal.MovementMode.MOVE_FLYING)
   check(name+'_aim',action(1));check(name+'_aim_walk',p.call_method('GetDesiredGait').value==0)
  elif phase==1:
   visual=p.call_method('GetActiveWeaponVisual');check(name+'_socket',str(visual.get_attach_socket_name())==name+'Grip_R');check(name+'_no_relative_offsets',prop(visual,'relative_location').length()<.01 and abs(prop(visual,'relative_rotation').pitch)<.01 and abs(prop(visual,'relative_rotation').yaw)<.01)
   aim=p.get_actor_location()+unreal.Vector(500,0,50)
   target=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,R+'Combat/BP_PistolTarget.BP_PistolTarget_C'))[state['weapon']]
   target.set_actor_location(aim,False,True);state['target']=target
   check(name+'_fire',action(2));check(name+'_consumes_one',prop(inv,'WeaponMagazines')[state['index']]==capacity-1)
   check(name+'_pellet_count',len(prop(p,'PublicShotEnds'))==(8 if name=='Shotgun' else 1))
   report[name+'_health']=prop(target,'Health');check(name+'_damage',prop(target,'Health')<100)
   if name=='Revolver':check('revolver_damage_55',abs(prop(target,'Health')-45)<.1)
   check(name+'_cooldown',not action(2));check(name+'_reload',action(3));check(name+'_cannot_fire_reloading',not action(2))
   state['next']=time.monotonic()+3.4
  elif phase==2:
   check(name+'_reload_finishes',not prop(inv,'Reloading'));check(name+'_reload_exact_mag',prop(inv,'WeaponMagazines')[state['index']]==capacity);check(name+'_reload_exact_reserve',inv.call_method('GetItemQuantity',(unreal.Name('Ammo.'+name),))==23)
   check(name+'_full_reload_rejected',not action(3));check(name+'_fire_after_reload',action(2));check(name+'_reload_to_cancel',action(3));check(name+'_holster',inv.call_method('TrySelectWeapon',(slot,state['uid'],prop(inv,'LayoutVersion'))));state['next']=time.monotonic()+3.4
  elif phase==3:
   check(name+'_cancel_preserves_ammo',inv.call_method('GetItemQuantity',(unreal.Name('Ammo.'+name),))==23);check(name+'_holster_blocks_fire',not action(2))
   state['target'].destroy_actor()
   if state['weapon']==0:state['weapon']=1;state['phase']=-1
   else:finish();return
  state['phase']+=1
  if phase not in [1,2]:state['next']=time.monotonic()+.7
 except Exception:report['error']=traceback.format_exc();finish()
extra_firearms_handle=unreal.register_slate_post_tick_callback(tick)
