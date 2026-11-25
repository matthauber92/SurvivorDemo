import unreal
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
for w in worlds:
 pc=unreal.GameplayStatics.get_player_controller(w,0);print('WORLD',w.get_name(),pc)
 if pc and pc.is_local_controller():
  pc.call_method('ToggleInventory');widget=pc.get_editor_property('InventoryWidget')
  print('OPEN',pc.get_editor_property('InventoryOpen'),'WIDGET',widget)
  if widget:
   print('NAMES',[str(x.get_text()) for x in widget.get_editor_property('NameLabels')]);print('COUNT',widget.get_editor_property('OccupiedLabel').get_text());print('FOCUS',widget.has_keyboard_focus())
