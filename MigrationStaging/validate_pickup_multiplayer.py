import unreal,json,time,builtins,traceback
from pathlib import Path
ROOT='/Game/AIExample/Items/'
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
server=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
client=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
host=unreal.GameplayStatics.get_player_pawn(server,0)
remote=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(server,unreal.Pawn) if not p.is_locally_controlled())
cp=unreal.GameplayStatics.get_player_pawn(client,0)
hpc=host.get_controller();cpc=cp.get_controller()
ic=unreal.load_class(None,ROOT+'BP_InventoryComponent.BP_InventoryComponent_C')
pic=unreal.load_class(None,ROOT+'BP_ItemPickup.BP_ItemPickup_C')
interactc=unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionComponent.BP_InteractionComponent_C')
dc=unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionTestDoor.BP_InteractionTestDoor_C')
hi=hpc.get_component_by_class(ic);ri=remote.get_controller().get_component_by_class(ic);ci=cpc.get_component_by_class(ic)
ammo=unreal.load_asset(ROOT+'DA_HandgunAmmo');key=unreal.load_asset(ROOT+'DA_Key');med=unreal.load_asset(ROOT+'DA_FirstAidKit')
subs=[s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if 'Transient' in s.get_path_name()]
action=unreal.load_asset('/Game/AIExample/Interaction/IA_SurvivorInteract')
report={'mode':'two-player listen-server PIE','checks':{},'snapshots':{}}
def check(n,v):
 report['checks'][n]=bool(v);unreal.log('PICKUP_CHECK '+n+' '+str(bool(v)))
def inventory(i):return {'ids':[str(x) for x in i.get_editor_property('ItemIDs')],'quantities':list(i.get_editor_property('Quantities'))}
def qty(i,id):return i.call_method('GetItemQuantity',(unreal.Name(id),))
def pickups(w):return unreal.GameplayStatics.get_all_actors_of_class(w,pic)
def at(w,x,y):return next((a for a in pickups(w) if abs(a.get_actor_location().x-x)<1 and abs(a.get_actor_location().y-y)<1),None)
def inject():
 for s in subs:s.inject_input_vector_for_action(action,unreal.Vector(1,0,0),[],[])
def pos(p,x,y):p.set_actor_location(unreal.Vector(x,y,90),False,True)
def aim(pc,yaw=0):pc.set_control_rotation(unreal.Rotator(pitch=0,yaw=yaw,roll=0))
def prompt(p):return str(p.get_component_by_class(interactc).get_editor_property('PromptText'))
def doorstate(opened):
 return all(d.get_editor_property('IsOpen')==opened and abs(d.get_editor_property('DoorHinge').get_editor_property('relative_rotation').yaw-(90 if opened else 0))<.1 for w in worlds for d in unreal.GameplayStatics.get_all_actors_of_class(w,dc))
pos(host,-180,0);pos(remote,-600,600);aim(hpc);aim(cpc)
state={'phase':0,'next':time.monotonic()+1}
def finish():
 report['passed']=all(report['checks'].values()) and 'error' not in report
 (Path(unreal.Paths.project_saved_dir())/'PickupValidation/multiplayer-result.json').write_text(json.dumps(report,indent=2))
 unreal.unregister_slate_post_tick_callback(pickup_test_handle)
 unreal.log('PICKUP_MULTIPLAYER_RESULT '+json.dumps(report))
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   check('six_pickups_visible_on_both',len(pickups(server))==6 and len(pickups(client))==6)
   check('all_client_definitions_resolved',all(a.get_editor_property('ItemDefinition') is not None for a in pickups(client)))
   check('host_pickup_prompt',prompt(host)=='Press E to collect Handgun Ammo')
   inject()
  elif phase==1:
   check('host_collected_ammo',qty(hi,'Ammo.Handgun')==30)
   check('host_pickup_disappears_for_both',at(server,0,0) is None and at(client,0,0) is None)
   report['snapshots']['host_after_ammo']=inventory(hi)
   pos(host,-600,-600);pos(remote,-180,300);aim(cpc)
  elif phase==2:
   check('client_pickup_prompt',prompt(cp)=='Press E to collect First Aid Kit')
   inject()
  elif phase==3:
   check('client_collected_medkit',qty(ri,'Medical.FirstAidKit')==1 and qty(ci,'Medical.FirstAidKit')==1)
   check('client_pickup_disappears_for_both',at(server,0,300) is None and at(client,0,300) is None)
   check('inventory_private_to_owner',len(unreal.GameplayStatics.get_all_actors_of_class(client,unreal.PlayerController))==1 and qty(ci,'Ammo.Handgun')==0 and qty(hi,'Medical.FirstAidKit')==0)
   check('owning_inventory_matches_server',inventory(ci)==inventory(ri))
   check('client_cannot_mutate_inventory',not ci.call_method('TryAddItem',(ammo,5)))
   pos(host,220,0);pos(remote,-600,600);aim(hpc)
  elif phase==4:inject()
  elif phase==5:
   check('ammo_stacks_across_slots',qty(hi,'Ammo.Handgun')==75 and inventory(hi)['quantities']==[60,15])
   check('second_ammo_removed_for_both',at(server,400,0) is None and at(client,400,0) is None)
   before=inventory(hi)
   check('zero_negative_and_null_rejected',not hi.call_method('TryAddItem',(ammo,0)) and not hi.call_method('TryAddItem',(ammo,-1)) and not hi.call_method('TryAddItem',(None,1)))
   check('oversized_add_is_atomic',not hi.call_method('TryAddItem',(ammo,9999)) and inventory(hi)==before)
   pos(host,220,250);pos(remote,220,350)
   race=at(server,400,300)
   first=race.call_method('TryInteract',(host,));second=race.call_method('TryInteract',(remote,))
   check('same_frame_two_players_only_one_wins',bool(first) and not second and qty(hi,'Key.Placeholder')+qty(ri,'Key.Placeholder')==1)
  elif phase==6:
   check('contested_pickup_removed_for_both',at(server,400,300) is None and at(client,400,300) is None)
   check('losing_player_not_awarded_item',qty(ci,'Key.Placeholder')==0)
   remaining_slots=8-len(inventory(hi)['ids'])
   check('can_fill_exact_capacity',hi.call_method('TryAddItem',(key,remaining_slots)) and len(inventory(hi)['ids'])==8)
   state['full_inventory']=inventory(hi)
   pos(host,220,-300);pos(remote,-600,600);aim(hpc)
  elif phase==7:
   check('full_inventory_prompt',prompt(host)=='Inventory full')
   inject()
  elif phase==8:
   check('full_inventory_does_not_consume_pickup',at(server,400,-300) is not None and at(client,400,-300) is not None and inventory(hi)==state['full_inventory'])
   target=at(server,400,-300)
   check('out_of_range_direct_pickup_rejected',not target.call_method('TryInteract',(remote,)))
   comp=remote.get_component_by_class(interactc)
   check('server_interaction_rejects_out_of_range',not comp.call_method('ValidateTarget',(target,unreal.Vector(100,-300,100),unreal.Vector(1,0,0))))
   comp=host.get_component_by_class(interactc)
   check('server_rejects_wrong_sightline',not comp.call_method('ValidateTarget',(target,unreal.Vector(220,-300,100),unreal.Vector(0,0,-1))))
   check('server_rejects_invalid_target',not comp.call_method('ValidateTarget',(None,unreal.Vector(),unreal.Vector(1,0,0))))
   check('server_rejects_spoofed_origin',not comp.call_method('ValidateTarget',(target,unreal.Vector(-2000,-300,100),unreal.Vector(1,0,0))))
   pos(host,620,0);aim(hpc)
  elif phase==9:
   check('door_prompt_preserved',prompt(host)=='Press E to Open Door')
   inject()
  elif phase==10:
   check('door_opens_for_both_even_with_full_inventory',doorstate(True))
   aim(hpc,-26.565)
  elif phase==11:inject()
  elif phase==12:
   check('door_closes_for_both',doorstate(False))
   report['snapshots']['host_final']=inventory(hi);report['snapshots']['client_final']=inventory(ci)
   finish();return
  state['phase']+=1;state['next']=time.monotonic()+1.2
 except Exception:
  report['error']=traceback.format_exc();finish()
pickup_test_handle=unreal.register_slate_post_tick_callback(tick)
builtins.pickup_test_handle=pickup_test_handle
