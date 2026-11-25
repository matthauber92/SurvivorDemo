import unreal,json,time,traceback
from pathlib import Path
out=Path(unreal.Paths.project_saved_dir())/'InventoryDragValidation';out.mkdir(exist_ok=True)
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False);sw=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority());cw=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
hpc=unreal.GameplayStatics.get_player_controller(sw,0);cpc=unreal.GameplayStatics.get_player_controller(cw,0);rpc=next(p.get_controller() for p in unreal.GameplayStatics.get_all_actors_of_class(sw,unreal.Pawn) if not p.is_locally_controlled())
hi=hpc.get_editor_property('InventoryComponent');ci=cpc.get_editor_property('InventoryComponent');ri=rpc.get_editor_property('InventoryComponent')
ammo=unreal.load_asset('/Game/AIExample/Items/DA_HandgunAmmo');med=unreal.load_asset('/Game/AIExample/Items/DA_FirstAidKit');key=unreal.load_asset('/Game/AIExample/Items/DA_Key')
report={'checks':{},'mode':'two-player listen-server PIE'}
def check(n,v):report['checks'][n]=bool(v);print(n,bool(v))
def layout(i):return list(i.get_editor_property('SlotOrder'))
def contents(i):return [str(x) for x in i.get_editor_property('ItemIDs')],list(i.get_editor_property('Quantities'))
def names(p):return [str(x.get_text()) for x in p.get_editor_property('InventoryWidget').get_editor_property('NameLabels')]
def move(i,s,t,id,q,v):return i.call_method('TryMoveSlot',(s,t,unreal.Name(id),q,v))
hi.call_method('TryAddItem',(ammo,75));hi.call_method('TryAddItem',(key,1));ri.call_method('TryAddItem',(med,3));ri.call_method('TryAddItem',(ammo,10));state={'phase':0,'next':time.monotonic()+1}
def finish():
 report['passed']=all(report['checks'].values()) and 'error' not in report;(out/'multiplayer-result.json').write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(drag_test_handle)
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   hpc.call_method('ToggleInventory');cpc.call_method('ToggleInventory')
   check('default_layout',layout(hi)==list(range(8)) and layout(ci)==list(range(8)))
   before=contents(hi);check('server_move_to_empty',move(hi,0,7,'Ammo.Handgun',60,0));check('contents_unchanged',contents(hi)==before)
   check('UI_empty_source_occupied_target',names(hpc)[0]=='EMPTY' and names(hpc)[7]=='Handgun Ammo')
   check('swap_occupied',move(hi,7,2,'Ammo.Handgun',60,1) and names(hpc)[7]=='Key' and names(hpc)[2]=='Handgun Ammo')
   check('layout_stays_permutation',sorted(layout(hi))==list(range(8)))
   expected=layout(hi)
   check('invalid_indices_rejected',not move(hi,-1,3,'Ammo.Handgun',60,2) and not move(hi,2,8,'Ammo.Handgun',60,2))
   check('empty_source_rejected',not move(hi,0,1,'Ammo.Handgun',60,2))
   check('same_slot_rejected',not move(hi,2,2,'Ammo.Handgun',60,2))
   check('stale_version_rejected',not move(hi,2,3,'Ammo.Handgun',60,0))
   check('wrong_item_quantity_rejected',not move(hi,2,3,'Medical.FirstAidKit',60,2) and not move(hi,2,3,'Ammo.Handgun',59,2))
   check('rejections_leave_state_unchanged',layout(hi)==expected and contents(hi)==before)
   check('client_cannot_directly_mutate',not move(ci,0,6,'Medical.FirstAidKit',3,0))
   report['native_client_RPC_test']='Covered separately by physical client mouse test; Python call_method runs in editor script context.'
  elif phase==1:
   check('owner_replication_matches',layout(ci)==layout(ri) and ci.get_editor_property('LayoutVersion')==ri.get_editor_property('LayoutVersion'))
   check('client_initial_UI',names(cpc)[0]=='First Aid Kit' and names(cpc)[1]=='Handgun Ammo')
   check('client_does_not_change_host',layout(hi)==[7,1,0,3,4,5,6,2])
   check('other_controller_has_no_widget',rpc.get_editor_property('InventoryWidget') is None)
   hi.call_method('TryAddItem',(med,1));check('pickup_add_after_reorder',names(hpc)[3]=='First Aid Kit')
   check('occupied_count',str(hpc.get_editor_property('InventoryWidget').get_editor_property('OccupiedLabel').get_text())=='4 / 8 SLOTS OCCUPIED')
   hpc.call_method('CloseInventory');hpc.call_method('ToggleInventory');check('layout_survives_reopen',names(hpc)[7]=='Key' and names(hpc)[2]=='Handgun Ammo')
   check('no_pause',not unreal.GameplayStatics.is_game_paused(sw) and not unreal.GameplayStatics.is_game_paused(cw))
   report['host_layout']=layout(hi);report['client_layout']=layout(ci)
   finish();return
  state['phase']+=1;state['next']=time.monotonic()+1.2
 except Exception:report['error']=traceback.format_exc();finish()
drag_test_handle=unreal.register_slate_post_tick_callback(tick)

