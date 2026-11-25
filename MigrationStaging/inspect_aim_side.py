import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];pc=unreal.GameplayStatics.get_player_controller(w,0)
unreal.SystemLibrary.execute_console_command(w,'ToggleDebugCamera',pc)
