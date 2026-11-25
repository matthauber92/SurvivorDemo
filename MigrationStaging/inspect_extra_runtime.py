import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);inv=p.get_controller().get_editor_property('InventoryComponent')
for n in ['ItemIDs','SlotOrder','BackpackInstances','EquipmentInstances','WeaponItemIDs','WeaponInstances','WeaponTypes','LayoutVersion']:print(n,inv.get_editor_property(n))
for o in unreal.ObjectIterator(unreal.NiagaraSystem):
 if 'NS_RevolverMuzzle' in o.get_path_name():
  for n in ['emitter_handles','exposed_parameters']:
   try:print(n,o.get_editor_property(n))
   except Exception as e:print(str(e))
