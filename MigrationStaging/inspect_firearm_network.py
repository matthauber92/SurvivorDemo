import unreal
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
 print('WORLD',w.get_path_name())
 for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter.BP_SurvivorInteractionCharacter_C')):
  print('P',p.get_name(),p.has_authority(),p.is_locally_controlled(),p.get_actor_location(),p.get_editor_property('PublicActiveSlot'),p.get_editor_property('PublicAiming'))
  pc=p.get_controller()
  if pc:
   inv=pc.get_editor_property('InventoryComponent');print('INV',inv.get_editor_property('ActiveWeaponInstance'),inv.get_editor_property('EquipmentInstances'),inv.call_method('GetActivePistolIndex'),'LOCAL',pc.is_local_controller())
