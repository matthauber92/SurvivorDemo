import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Character) if 'Survivor' in p.get_class().get_name());p.get_editor_property('SidearmVisual').set_relative_rotation(unreal.Rotator(0,180,-90),False,True)
