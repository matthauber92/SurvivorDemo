import unreal
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
 pc=unreal.GameplayStatics.get_player_controller(w,0);u=pc.get_editor_property('InventoryWidget')
 print('FOCUSABLE',u.get_editor_property('is_focusable'),'FOCUS',u.has_user_focus(pc))
 print('KEYS',u.get_editor_property('ToggleKey'),u.get_editor_property('CloseKey'))
 if pc.has_authority():
  inv=pc.get_editor_property('InventoryComponent');print('ADD',inv.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_HandgunAmmo'),75)))
  print('TEXT',[str(x.get_text()) for x in u.get_editor_property('NameLabels')],[str(x.get_text()) for x in u.get_editor_property('QuantityLabels')])
