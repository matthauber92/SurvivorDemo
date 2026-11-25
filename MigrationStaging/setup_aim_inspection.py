import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();inv=pc.get_editor_property('InventoryComponent')
assert inv.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_PistolItem'),1))
uid=inv.get_editor_property('BackpackInstances')[0]
assert inv.call_method('TryTransferWeapon',(0,10,uid,inv.get_editor_property('LayoutVersion')))
assert inv.call_method('TrySelectWeapon',(2,uid,inv.get_editor_property('LayoutVersion')))
p.set_actor_location(unreal.Vector(-1000,-1000,90),False,True);pc.set_control_rotation(unreal.Rotator())
assert inv.call_method('TryPistolAction',(1,uid,p.get_actor_location(),unreal.Vector(1,0,0)))
mesh=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin')
s=mesh.find_socket('PistolGrip_R');print('GRIP',s.get_editor_property('relative_location'),s.get_editor_property('relative_rotation'))
