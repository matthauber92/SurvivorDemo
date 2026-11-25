import unreal
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
sw=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority());cw=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
remote=next(p.get_controller() for p in unreal.GameplayStatics.get_all_actors_of_class(sw,unreal.Pawn) if not p.is_locally_controlled())
inv=remote.get_editor_property('InventoryComponent')
assert not inv.get_editor_property('ItemIDs')
for name,amount in [('DA_PistolItem',2),('DA_EquipmentTestLongGun',2),('DA_HandgunAmmo',10)]:assert inv.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/'+name),amount))
unreal.GameplayStatics.get_player_controller(cw,0).call_method('ToggleInventory')
print('CLIENT_WEAPON_DRAG_TEST_READY')
