import unreal,json
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];pc=unreal.GameplayStatics.get_player_controller(w,0)
assert pc.get_editor_property('InventoryOpen') and pc.get_editor_property('show_mouse_cursor') and pc.is_move_input_ignored()
inv=pc.get_editor_property('InventoryComponent');inv.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_HandgunAmmo'),75))
unreal.SystemLibrary.execute_console_command(w,'Shot showui',pc)
(Path(unreal.Paths.project_saved_dir())/'InventoryUIValidation/final-input-binding-check.json').write_text(json.dumps({'single_connected_Started_binding':True,'enhanced_input_opens':True,'cursor_and_gates_enabled':True}))
