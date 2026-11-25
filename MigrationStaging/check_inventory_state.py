import unreal
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
 p=unreal.GameplayStatics.get_player_controller(w,0)
 print('STATE',w.get_path_name(),p.get_editor_property('InventoryOpen'),p.get_editor_property('show_mouse_cursor'),p.is_move_input_ignored(),p.is_look_input_ignored())
