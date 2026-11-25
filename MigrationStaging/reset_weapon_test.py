import unreal
ws=unreal.EditorLevelLibrary.get_pie_worlds(False)
sw=next(w for w in ws if unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
p=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(sw,unreal.Pawn) if not p.is_locally_controlled());i=p.get_controller().get_editor_property('InventoryComponent')
if i.get_editor_property('ActiveWeaponInstance'):i.call_method('TrySelectWeapon',(p.get_editor_property('PublicActiveSlot'),i.get_editor_property('ActiveWeaponInstance'),i.get_editor_property('LayoutVersion')))
