import unreal,json,time,traceback
from pathlib import Path
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
sw=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority());cw=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
hpc=unreal.GameplayStatics.get_player_controller(sw,0);cpc=unreal.GameplayStatics.get_player_controller(cw,0)
rpc=next(p.get_controller() for p in unreal.GameplayStatics.get_all_actors_of_class(sw,unreal.Pawn) if not p.is_locally_controlled())
hi=hpc.get_editor_property('InventoryComponent');ci=cpc.get_editor_property('InventoryComponent');ri=rpc.get_editor_property('InventoryComponent')
report={'checks':{},'mode':'two-player listen-server PIE'};state={'phase':0,'next':time.monotonic()+1}
def a(i,n):return list(i.get_editor_property(n))
def v(i):return i.get_editor_property('LayoutVersion')
def check(n,b):
 report['checks'][n]=bool(b)
 assert b,n
def snapshot(i):return {n:[str(x) for x in a(i,n)] for n in ['ItemIDs','Quantities','SlotOrder','BackpackInstances','EquipmentInstances','WeaponInstances','WeaponItemIDs','WeaponTypes','WeaponMagazines']}
def finish():
 report['passed']=all(report['checks'].values()) and 'error' not in report
 (Path(unreal.Paths.project_saved_dir())/'EquipmentValidation/multiplayer-result.json').write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(equipment_net_handle)
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   check('host_and_client_start_empty',not a(hi,'ItemIDs') and not a(ci,'ItemIDs') and a(hi,'EquipmentInstances')==a(ci,'EquipmentInstances')==['','',''])
   pistol=unreal.load_asset('/Game/AIExample/Items/DA_PistolItem');longgun=unreal.load_asset('/Game/AIExample/Items/DA_EquipmentTestLongGun')
   fixtures=[]
   for definition,mag in [(pistol,6),(longgun,17)]:
    fixture=unreal.new_object(definition.get_class())
    for k in ['ItemID','Category','EquipmentType','MaxStackSize']:fixture.set_editor_property(k,definition.get_editor_property(k))
    fixture.set_editor_property('InitialMagazine',mag);fixtures.append(fixture)
   check('independent_pickups',hi.call_method('TryAddItem',(fixtures[1],1)) and ri.call_method('TryAddItem',(fixtures[0],2)))
  elif phase==1:
   check('owner_state_replication',snapshot(ci)==snapshot(ri));hpc.call_method('ToggleInventory');cpc.call_method('ToggleInventory')
   uid=a(ci,'BackpackInstances')[0];state['uid']=uid
   check('direct_client_mutation_rejected',not ci.call_method('TryTransferWeapon',(0,10,uid,v(ci))))
   before=v(ri);check('first_server_request',ri.call_method('TryTransferWeapon',(0,10,uid,before)))
   check('simultaneous_duplicate_request_rejected',not ri.call_method('TryTransferWeapon',(0,10,uid,before)))
   hu=a(hi,'BackpackInstances')[0];check('host_equips_independently',hi.call_method('TryTransferWeapon',(0,8,hu,v(hi))))
  elif phase==2:
   check('equipment_replication',snapshot(ci)==snapshot(ri) and a(ci,'EquipmentInstances')[2]==state['uid'])
   check('host_client_independence',a(hi,'WeaponInstances')!=a(ci,'WeaponInstances') and a(hi,'EquipmentInstances')[2]=='' and a(ci,'EquipmentInstances')[0]=='')
   check('owner_UI_updates',str(cpc.get_editor_property('InventoryWidget').get_editor_property('EquipmentNames')[2].get_text())=='Pistol')
   check('magazine_values_replicated',a(ci,'WeaponMagazines')==[6,6] and a(hi,'WeaponMagazines')==[17])
   check('other_inventory_not_on_client',len(unreal.GameplayStatics.get_all_actors_of_class(cw,cpc.get_class()))==1)
   check('no_duplication_loss',sorted(x for x in a(ri,'BackpackInstances')+a(ri,'EquipmentInstances') if x)==sorted(a(ri,'WeaponInstances')))
   report['native_client_rpc']='Physical client click verification is separate; this suite exercises authoritative transactions and owner replication.'
   report['host']=snapshot(hi);report['client']=snapshot(ci);finish();return
  state['phase']+=1;state['next']=time.monotonic()+1.5
 except Exception:report['error']=traceback.format_exc();finish()
equipment_net_handle=unreal.register_slate_post_tick_callback(tick)
