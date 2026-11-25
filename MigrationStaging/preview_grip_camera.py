import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller()
unreal.SystemLibrary.execute_console_command(w,'ToggleDebugCamera',pc)
print('DEBUG',unreal.GameplayStatics.get_all_actors_of_class(w,unreal.DebugCameraController))
