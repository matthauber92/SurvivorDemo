import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Character) if 'Survivor' in p.get_class().get_name());i=p.get_controller().get_editor_property('InventoryComponent');i.call_method('TrySelectWeapon',(2,i.get_editor_property('EquipmentInstances')[2],i.get_editor_property('LayoutVersion')))
