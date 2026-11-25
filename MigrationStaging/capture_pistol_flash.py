import unreal,time
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Character) if 'Survivor' in p.get_class().get_name());i=p.get_controller().get_editor_property('InventoryComponent');d=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.DebugCameraController)[0]
print('FIRE',i.call_method('TryPistolAction',(2,i.get_editor_property('ActiveWeaponInstance'),p.get_actor_location()+unreal.Vector(0,0,60),p.get_actor_forward_vector())))
unreal.SystemLibrary.execute_console_command(w,'Shot',d)
