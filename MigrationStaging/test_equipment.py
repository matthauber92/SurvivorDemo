import unreal,json,traceback
from pathlib import Path
R='/Game/AIExample/';out=Path(unreal.Paths.project_saved_dir())/'EquipmentValidation'
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];pc=unreal.GameplayStatics.get_player_controller(w,0);inv=pc.get_editor_property('InventoryComponent')
report={'checks':{},'mode':'single-player PIE'}
def check(n,v):
 report['checks'][n]=bool(v)
 assert v,n
def a(n):return list(inv.get_editor_property(n))
def version():return inv.get_editor_property('LayoutVersion')
def instance(loc):return inv.call_method('GetInstanceAtLocation',(loc,))
def loc(uid):return next(i for i in range(11) if instance(i)==uid)
def transfer(uid,target):return inv.call_method('TryTransferWeapon',(loc(uid),target,uid,version()))
def add(name,n=1):
 definition=unreal.load_asset(R+'Items/'+name)
 if name in ['DA_PistolItem','DA_EquipmentTestLongGun']:
  fixture=unreal.new_object(definition.get_class())
  for k in ['ItemID','Category','EquipmentType','MaxStackSize']:fixture.set_editor_property(k,definition.get_editor_property(k))
  fixture.set_editor_property('InitialMagazine',7 if name=='DA_PistolItem' else 19);definition=fixture
 return inv.call_method('TryAddItem',(definition,n))
def snapshot():return {n:[str(x) for x in a(n)] for n in ['ItemIDs','Quantities','SlotOrder','BackpackInstances','EquipmentInstances','WeaponInstances','WeaponItemIDs','WeaponTypes','WeaponMagazines']}
def conserved():
 ids=[s for s in a('BackpackInstances')+a('EquipmentInstances') if s]
 return len(ids)==len(set(ids)) and sorted(ids)==sorted(a('WeaponInstances')) and sorted(a('SlotOrder'))==list(range(8)) and len(a('ItemIDs'))==len(a('BackpackInstances'))==len(a('Quantities'))<=8
try:
 check('starts_empty',a('EquipmentInstances')==['','',''] and not a('ItemIDs'))
 check('pickup_pistols_and_long_guns',add('DA_PistolItem',2) and add('DA_EquipmentTestLongGun',2))
 p1,p2,l1,l2=a('BackpackInstances');check('unique_instances',len(set([p1,p2,l1,l2]))==4)
 check('magazines_initialized',a('WeaponMagazines')==[7,7,19,19]);records=snapshot()
 pc.call_method('ToggleInventory');ui=pc.get_editor_property('InventoryWidget')
 check('three_equipment_eight_backpack_widgets',len(ui.get_editor_property('EquipmentFrames'))==3 and len(ui.get_editor_property('SlotFrames'))==8)
 check('pistol_to_sidearm',transfer(p1,10));check('equip_frees_backpack',len(a('ItemIDs'))==3)
 before=snapshot();check('pistol_rejected_primary',not transfer(p2,8));check('invalid_unchanged',snapshot()==before)
 check('long_gun_primary',transfer(l1,8));check('long_gun_secondary',transfer(l2,9))
 check('equipment_swap',transfer(l1,9) and instance(8)==l2 and instance(9)==l1)
 check('backpack_equipment_swap',transfer(p2,10) and instance(10)==p2 and instance(loc(p1))==p1)
 check('equipment_backpack_swap',transfer(p2,loc(p1)) and instance(10)==p1)
 before=snapshot();check('incompatible_equipment_swap',not transfer(p1,8) and before==snapshot())
 check('unequip',transfer(l2,-1) and len(a('ItemIDs'))==2)
 check('re_equip',transfer(l2,8))
 check('fill_backpack',add('DA_Key',7) and len(a('ItemIDs'))==8)
 before=snapshot();check('full_backpack_rejects_unequip',not transfer(l1,-1) and snapshot()==before)
 check('full_backpack_atomic_swap',transfer(p2,10) and len(a('ItemIDs'))==8)
 check('capacity_rejects_pickup',not add('DA_PistolItem'))
 before=snapshot();keyloc=next(i for i in range(8) if not instance(i))
 check('cannot_swap_equipment_with_key',not transfer(l1,keyloc) and snapshot()==before)
 source=loc(p1);v=version();check('first_duplicate_request_succeeds',inv.call_method('TryTransferWeapon',(source,10,p1,v)))
 before=snapshot();check('duplicate_stale_request_rejected',not inv.call_method('TryTransferWeapon',(source,10,p1,v)) and snapshot()==before)
 check('invalid_location_rejected',not inv.call_method('TryTransferWeapon',(-2,10,p1,version())))
 check('weapon_records_and_magazines_preserved',all(snapshot()[n]==records[n] for n in ['WeaponInstances','WeaponItemIDs','WeaponTypes','WeaponMagazines']))
 check('no_duplication_loss_or_capacity_corruption',conserved())
 check('occupied_equipment_labels',[str(x.get_text()) for x in ui.get_editor_property('EquipmentNames')]==['Long gun (test)','Long gun (test)','Pistol'])
 pc.call_method('CloseInventory');pc.call_method('ToggleInventory');check('reopen_preserves_equipment',conserved() and len(pc.get_editor_property('InventoryWidget').get_editor_property('EquipmentFrames'))==3)
 report['final']=snapshot()
except Exception:report['error']=traceback.format_exc()
report['passed']=all(report['checks'].values()) and 'error' not in report
(out/'singleplayer-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
