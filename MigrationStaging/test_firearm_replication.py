import unreal,time,json,traceback
from pathlib import Path
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False);sw=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority());cw=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
cp=unreal.GameplayStatics.get_player_pawn(cw,0);cpc=cp.get_controller();ci=cpc.get_editor_property('InventoryComponent');sp=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(sw,cp.get_class()) if not p.is_locally_controlled());si=sp.get_controller().get_editor_property('InventoryComponent')
report={'checks':{}};state={'weapon':0,'phase':0,'next':time.monotonic()+1};out=Path(unreal.Paths.project_saved_dir())/'firearm-multiplayer-result.json';R='/Game/AIExample/'
inputs=[s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if 'Transient' in s.get_path_name()]
assert len(inputs)==2,len(inputs)
def inject(name):
 for s in inputs:s.inject_input_vector_for_action(unreal.load_asset(R+'Combat/IA_Pistol'+name),unreal.Vector(1,0,0),[],[])
def check(n,v):report['checks'][n]=bool(v);assert v,n
def finish():
 report['passed']='error' not in report and all(report['checks'].values());out.write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(firearm_rep_handle)
def prop(o,n):return o.get_editor_property(n)
def tick(dt):
 if state.get('hold_aim'):inject('Aim')
 if time.monotonic()<state['next']:return
 try:
  name=['Revolver','Shotgun'][state['weapon']];slot=2 if name=='Revolver' else 0;phase=state['phase'];capacity=6 if name=='Revolver' else 2
  if phase==0:
   assert si.call_method('TryAddItem',(unreal.load_asset(R+'Items/DA_'+name+'Item'),1));assert si.call_method('TryAddItem',(unreal.load_asset(R+'Items/DA_'+name+'Ammo'),12))
   ix=list(prop(si,'ItemIDs')).index(unreal.Name('Weapon.'+name));uid=prop(si,'BackpackInstances')[ix];state['uid']=uid
   assert si.call_method('TryTransferWeapon',(list(prop(si,'SlotOrder')).index(ix),8+slot,uid,prop(si,'LayoutVersion')));assert si.call_method('TrySelectWeapon',(slot,uid,prop(si,'LayoutVersion')))
   sp.set_actor_location(unreal.Vector(0,0,2000),False,True);sp.character_movement.set_movement_mode(unreal.MovementMode.MOVE_FLYING)
   target=unreal.GameplayStatics.get_all_actors_of_class(sw,unreal.load_class(None,R+'Combat/BP_PistolTarget.BP_PistolTarget_C'))[state['weapon']];target.set_actor_location(unreal.Vector(500,0,2050),False,True);state['target']=target
  elif phase==1:
   check(name+'_equipment_replicated',str(prop(cp,'PublicSidearm' if slot==2 else 'PublicPrimary'))=='Weapon.'+name and prop(cp,'PublicActiveSlot')==slot)
   check(name+'_socket_on_client',str(cp.call_method('GetActiveWeaponVisual').get_attach_socket_name())==name+'Grip_R')
   cpc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(unreal.GameplayStatics.get_player_camera_manager(cw,0).get_camera_location(),state['target'].get_actor_location()));state['hold_aim']=True
  elif phase==2:
   check(name+'_aim_replicated',prop(sp,'PublicAiming') and prop(cp,'PublicAiming'))
   inject('Fire')
  elif phase==3:
   index=si.call_method('GetActivePistolIndex');check(name+'_server_spends_round',prop(si,'WeaponMagazines')[index]==capacity-1);check(name+'_client_mag_replicated',prop(ci,'WeaponMagazines')[index]==capacity-1)
   check(name+'_server_applies_damage',prop(state['target'],'Health')<100)
   check(name+'_shot_event_replicated',prop(cp,'PublicShotSerial')==prop(sp,'PublicShotSerial') and prop(cp,'PublicShotSerial')>0)
   check(name+'_pellet_endpoints_replicated',len(prop(cp,'PublicShotEnds'))==(1 if name=='Revolver' else 8))
   inject('Reload');state['next']=time.monotonic()+3.6
  elif phase==4:
   state['hold_aim']=False
   check(name+'_reload_replicated',prop(si,'WeaponMagazines')==prop(ci,'WeaponMagazines') and prop(si,'WeaponMagazines')[si.call_method('GetActivePistolIndex')]==capacity)
   check(name+'_reserve_replicated',ci.call_method('GetItemQuantity',(unreal.Name('Ammo.'+name),))==11)
   if state['weapon']==0:state['weapon']=1;state['phase']=-1
   else:finish();return
  state['phase']+=1
  if phase!=3:state['next']=time.monotonic()+.8
 except Exception:report['error']=traceback.format_exc();finish()
firearm_rep_handle=unreal.register_slate_post_tick_callback(tick)
