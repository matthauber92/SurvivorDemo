import unreal,time,json,traceback
from pathlib import Path
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
sw=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority());cw=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
hpc=unreal.GameplayStatics.get_player_controller(sw,0);hp=hpc.get_controlled_pawn();hi=hpc.get_editor_property('InventoryComponent')
report={'checks':{}};state={'phase':0,'next':time.monotonic()+.5}
def check(n,b):report['checks'][n]=bool(b);assert b,n
def finish():
 report['passed']=all(report['checks'].values()) and 'error' not in report
 (Path(unreal.Paths.project_saved_dir())/'WeaponSwitchValidation/observer-result.json').write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(weapon_observer_handle)
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   if not hi.get_editor_property('WeaponInstances'):assert hi.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_PistolItem'),1))
   uid=hi.get_editor_property('WeaponInstances')[0];state['uid']=uid
   if hi.get_editor_property('EquipmentInstances')[2]!=uid:assert hi.call_method('TryTransferWeapon',(0,10,uid,hi.get_editor_property('LayoutVersion')))
   if hi.get_editor_property('ActiveWeaponInstance')!=uid:assert hi.call_method('TrySelectWeapon',(2,uid,hi.get_editor_property('LayoutVersion')))
  elif phase==1:
   observer=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(cw,hp.get_class()) if not p.is_locally_controlled())
   check('other_player_sees_host_draw',observer.get_editor_property('PublicActiveSlot')==2 and not observer.get_editor_property('SidearmVisual').get_editor_property('hidden_in_game'))
   check('observer_pistol_attached_to_hand',str(observer.get_editor_property('SidearmVisual').get_attach_socket_name())=='hand_r')
   transform=hp.get_actor_transform();transform.translation=transform.translation+unreal.Vector(0,0,20)
   hpc.un_possess();hp.destroy_actor()
   unreal.GameplayStatics.get_game_mode(sw).restart_player_at_transform(hpc,transform)
   state['newpawn']=hpc.get_controlled_pawn()
  elif phase==2:
   check('respawn_resets_to_holstered',hi.get_editor_property('ActiveWeaponInstance')=='' and state['newpawn'].get_editor_property('PublicActiveSlot')==-1)
   check('respawn_preserves_equipment',hi.get_editor_property('EquipmentInstances')[2]==state['uid'] and str(state['newpawn'].get_editor_property('PublicSidearm'))=='Weapon.Pistol')
   assert hi.call_method('TrySelectWeapon',(2,state['uid'],hi.get_editor_property('LayoutVersion')))
  elif phase==3:
   observer=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(cw,state['newpawn'].get_class()) if not p.is_locally_controlled())
   check('respawned_weapon_draw_replicates',observer.get_editor_property('PublicActiveSlot')==2)
   finish();return
  state['phase']+=1;state['next']=time.monotonic()+1
 except Exception:report['error']=traceback.format_exc();finish()
weapon_observer_handle=unreal.register_slate_post_tick_callback(tick)

