import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Character) if 'Survivor' in p.get_class().get_name());pc=p.get_controller();inv=pc.get_editor_property('InventoryComponent');uid=inv.get_editor_property('EquipmentInstances')[0]
assert inv.call_method('TrySelectWeapon',(0,uid,inv.get_editor_property('LayoutVersion')))
assert inv.call_method('TryPistolAction',(1,uid,p.get_actor_location(),unreal.Vector(1,0,0)))
print('SHOTGUN POSE',p.mesh.get_anim_instance().get_class().get_path_name())
