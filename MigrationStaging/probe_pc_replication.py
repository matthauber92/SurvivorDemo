import unreal
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
 p=unreal.GameplayStatics.get_player_controller(w,0);print('REPLICATES',p.has_authority(),p.get_editor_property('replicates'))
 if not p.has_authority():
  p.set_editor_property('replicates',True)
  p.call_method('RequestMoveInventory',(0,6,unreal.Name('Medical.FirstAidKit'),3,0))
