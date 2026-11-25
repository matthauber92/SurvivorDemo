import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();i=pc.get_editor_property('InventoryComponent')
for name,num in [('DA_PistolItem',1),('DA_HandgunAmmo',30)]:assert i.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/'+name),num))
uid=i.get_editor_property('BackpackInstances')[0];assert i.call_method('TryTransferWeapon',(0,10,uid,i.get_editor_property('LayoutVersion')))
p.set_actor_location(unreal.Vector(0,800,88),False,True);pc.set_control_rotation(unreal.Rotator())
