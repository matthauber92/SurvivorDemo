import unreal,json,time,traceback
from pathlib import Path
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
sw=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority());cw=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
host=unreal.GameplayStatics.get_player_pawn(sw,0);client=unreal.GameplayStatics.get_player_pawn(cw,0)
hpc=host.get_controller();cpc=client.get_controller();remote=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(sw,unreal.Pawn) if not p.is_locally_controlled());rpc=remote.get_controller()
hi=hpc.get_editor_property('InventoryComponent');ci=cpc.get_editor_property('InventoryComponent');ri=rpc.get_editor_property('InventoryComponent')
ammo=unreal.load_asset('/Game/AIExample/Items/DA_HandgunAmmo');med=unreal.load_asset('/Game/AIExample/Items/DA_FirstAidKit')
report={'mode':'two-player listen-server PIE','checks':{}}
def check(n,v):report['checks'][n]=bool(v);print('UI_MULTIPLAYER',n,bool(v))
def labels(pc):
 widget=pc.get_editor_property('InventoryWidget')
 return {'names':[str(x.get_text()) for x in widget.get_editor_property('NameLabels')],'quantities':[str(x.get_text()) for x in widget.get_editor_property('QuantityLabels')],'count':str(widget.get_editor_property('OccupiedLabel').get_text())}
def inject(action):
 for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem):
  if 'Transient' in s.get_path_name():s.inject_input_vector_for_action(unreal.load_asset(action),unreal.Vector(1,0,0),[],[])
def finish():
 report['passed']=all(report['checks'].values()) and 'error' not in report
 (Path(unreal.Paths.project_saved_dir())/'InventoryUIValidation/multiplayer-result.json').write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(ui_multi_handle);print('UI_MULTIPLAYER_RESULT',json.dumps(report))
host.set_actor_location(unreal.Vector(-600,-600,90),False,True);remote.set_actor_location(unreal.Vector(-180,300,90),False,True);cpc.set_control_rotation(unreal.Rotator())
state={'phase':0,'next':time.monotonic()+1}
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   hpc.call_method('ToggleInventory')
   check('host_open_client_closed',hpc.get_editor_property('InventoryOpen') and not cpc.get_editor_property('InventoryOpen'))
   check('host_eight_empty_slots',labels(hpc)['names']==['EMPTY']*8)
   state['server_time']=unreal.GameplayStatics.get_time_seconds(sw);state['client_time']=unreal.GameplayStatics.get_time_seconds(cw)
   inject('/Game/AIExample/Interaction/IA_SurvivorInteract')
  elif phase==1:
   check('client_collects_while_host_inventory_open',list(ci.get_editor_property('Quantities'))==[1] and list(ri.get_editor_property('Quantities'))==[1])
   check('host_did_not_receive_client_item',list(hi.get_editor_property('Quantities'))==[] and labels(hpc)['count']=='0 / 8 SLOTS OCCUPIED')
   check('both_worlds_continue',unreal.GameplayStatics.get_time_seconds(sw)>state['server_time']+.5 and unreal.GameplayStatics.get_time_seconds(cw)>state['client_time']+.5)
   check('neither_world_paused',not unreal.GameplayStatics.is_game_paused(sw) and not unreal.GameplayStatics.is_game_paused(cw))
   cpc.call_method('ToggleInventory')
   check('client_UI_reads_existing_owner_inventory',labels(cpc)['names'][0]=='First Aid Kit' and labels(cpc)['quantities'][0]=='1')
   check('distinct_widgets_and_sources',hpc.get_editor_property('InventoryWidget')!=cpc.get_editor_property('InventoryWidget') and cpc.get_editor_property('InventoryWidget').get_editor_property('InventorySource')==ci)
   check('remote_server_controller_has_no_UI',rpc.get_editor_property('InventoryWidget') is None and not rpc.get_editor_property('InventoryOpen'))
   check('client_has_only_own_controller',len(unreal.GameplayStatics.get_all_actors_of_class(cw,unreal.PlayerController))==1)
   check('client_mutation_still_rejected',not ci.call_method('TryAddItem',(ammo,99)))
   hi.call_method('TryAddItem',(ammo,75));ri.call_method('TryAddItem',(med,6))
  elif phase==2:
   check('host_live_stack_refresh',labels(hpc)['quantities'][:2]==['60','15'])
   check('client_repnotify_live_stack_refresh',labels(cpc)['names'][:2]==['First Aid Kit','First Aid Kit'] and labels(cpc)['quantities'][:2]==['5','2'])
   check('host_client_content_private',labels(hpc)['names'][0]=='Handgun Ammo' and labels(cpc)['names'][0]=='First Aid Kit')
   check('owner_replica_matches_authority',list(ci.get_editor_property('ItemIDs'))==list(ri.get_editor_property('ItemIDs')) and list(ci.get_editor_property('Quantities'))==list(ri.get_editor_property('Quantities')))
   report['host']=labels(hpc);report['client']=labels(cpc)
   cpc.call_method('CloseInventory')
   check('client_close_does_not_close_host',not cpc.get_editor_property('InventoryOpen') and hpc.get_editor_property('InventoryOpen'))
   check('client_input_restored_host_still_gated',not cpc.is_move_input_ignored() and not cpc.is_look_input_ignored() and not cpc.get_editor_property('show_mouse_cursor') and hpc.is_move_input_ignored())
   hpc.call_method('CloseInventory');check('host_input_restored',not hpc.is_move_input_ignored() and not hpc.is_look_input_ignored() and not hpc.get_editor_property('show_mouse_cursor'))
   finish();return
  state['phase']+=1;state['next']=time.monotonic()+1.2
 except Exception:report['error']=traceback.format_exc();finish()
ui_multi_handle=unreal.register_slate_post_tick_callback(tick)
