import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
print('STRUCT_API',[n for n in dir(unreal.InstancedStruct) if not n.startswith('_')])
for a in unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_class(unreal.TopLevelAssetPath('/Script/Chooser','ChooserTable'),True):
 if 'PoseSearchDatabases' in str(a.package_name):
  o=a.get_asset();print('CHOOSER',o.get_path_name(),o.get_editor_property('context_data'))
  for c in o.get_editor_property('context_data'):print('CONTEXT',c.export_text())
