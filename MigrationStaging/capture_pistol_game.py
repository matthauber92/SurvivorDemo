import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];d=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.DebugCameraController)[0]
unreal.SystemLibrary.execute_console_command(w,'Shot',d)
