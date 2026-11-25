import unreal
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
 pc=unreal.GameplayStatics.get_player_controller(w,0);ui=pc.get_editor_property('InventoryWidget')
 print('UI',pc.has_authority(),ui.is_in_viewport(),ui.get_visibility(),unreal.SlateLibrary.get_local_size(ui.get_cached_geometry()))
 for f in list(ui.get_editor_property('SlotFrames'))[:1]:print('SLOT',f.get_path_name(),unreal.SlateLibrary.get_local_size(f.get_cached_geometry()))
 if not pc.has_authority():unreal.SystemLibrary.execute_console_command(w,'Shot showui',pc)
