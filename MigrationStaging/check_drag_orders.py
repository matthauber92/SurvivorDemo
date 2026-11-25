import unreal
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
 for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PlayerController):
  print(p.has_authority(),p.is_local_controller(),p.get_editor_property('InventoryComponent').get_editor_property('SlotOrder'))
