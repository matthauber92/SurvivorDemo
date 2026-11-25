import unreal
reg=unreal.AssetRegistryHelpers.get_asset_registry()
for a in reg.get_assets_by_class(unreal.TopLevelAssetPath('/Script/EnhancedInput','InputMappingContext'),True):
 if not str(a.package_name).startswith('/Game/'):continue
 c=a.get_asset()
 for m in c.get_editor_property('default_key_mappings').get_editor_property('mappings'):
  if str(m.get_editor_property('key').export_text()) in ['I','Escape']:print(c.get_path_name(),m.export_text())
