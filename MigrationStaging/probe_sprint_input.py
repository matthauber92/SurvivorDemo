import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0)
print('STATE',p.get_editor_property('CharacterInputState'),p.get_editor_property('Gait'),p.get_velocity())
for a in unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_class(unreal.TopLevelAssetPath('/Script/EnhancedInput','InputMappingContext'),True):
 obj=a.get_asset()
 print(obj.get_path_name(),[(str(m.get_editor_property('key').export_text()),str(m.get_editor_property('action'))) for m in obj.get_editor_property('default_key_mappings').get_editor_property('mappings')])
