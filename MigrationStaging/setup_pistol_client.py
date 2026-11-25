import unreal
ws=unreal.EditorLevelLibrary.get_pie_worlds(False);sw=next(w for w in ws if unreal.GameplayStatics.get_player_pawn(w,0).has_authority());cw=next(w for w in ws if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
host=unreal.GameplayStatics.get_player_pawn(sw,0);p=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(sw,host.get_class()) if not p.is_locally_controlled());i=p.get_controller().get_editor_property('InventoryComponent')
for name,num in [('DA_PistolItem',1),('DA_HandgunAmmo',30)]:assert i.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/'+name),num))
uid=i.get_editor_property('BackpackInstances')[0];assert i.call_method('TryTransferWeapon',(0,10,uid,i.get_editor_property('LayoutVersion')))
p.set_actor_location(unreal.Vector(0,800,88),False,True);host.set_actor_location(unreal.Vector(-500,400,88),False,True)
unreal.GameplayStatics.get_player_controller(cw,0).set_control_rotation(unreal.Rotator())
