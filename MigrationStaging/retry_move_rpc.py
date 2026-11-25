import unreal
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
 p=unreal.GameplayStatics.get_player_controller(w,0)
 if not p.has_authority():
  i=p.get_editor_property('InventoryComponent');print('BEFORE',p.is_local_controller(),i.get_editor_property('LayoutVersion'),i.get_editor_property('SlotOrder'))
  p.call_method('RequestMoveInventory',(6,5,unreal.Name('Medical.FirstAidKit'),3,1))
