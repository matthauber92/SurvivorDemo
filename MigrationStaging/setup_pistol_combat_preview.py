import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);i=p.get_controller().get_editor_property('InventoryComponent')
for name,num in [('DA_PistolItem',1),('DA_HandgunAmmo',30)]:assert i.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/'+name),num))
uid=i.get_editor_property('BackpackInstances')[0];assert i.call_method('TryTransferWeapon',(0,10,uid,i.get_editor_property('LayoutVersion')));assert i.call_method('TrySelectWeapon',(2,uid,i.get_editor_property('LayoutVersion')))
print('ANIMCLASS',p.get_component_by_class(unreal.SkeletalMeshComponent).get_anim_instance().get_class().get_name())
print('RELOAD_STARTED',i.call_method('TryPistolAction',(3,uid,unreal.Vector(),unreal.Vector(1,0,0))))
