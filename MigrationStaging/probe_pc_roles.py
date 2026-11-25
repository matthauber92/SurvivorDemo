import unreal
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
 p=unreal.GameplayStatics.get_player_controller(w,0);print('PC',p.has_authority(),p.get_editor_property('replicates'),p.get_local_role(),p.get_remote_role())
