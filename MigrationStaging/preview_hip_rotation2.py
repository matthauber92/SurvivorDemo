import unreal
print('ROT',unreal.Rotator(0,180,-90),unreal.Rotator(pitch=0,yaw=180,roll=-90))
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Character) if 'Survivor' in p.get_class().get_name());c=p.get_editor_property('SidearmVisual');print('OLD',c.get_editor_property('relative_rotation'));c.set_relative_rotation(unreal.Rotator(pitch=0,yaw=180,roll=-90),False,True)
