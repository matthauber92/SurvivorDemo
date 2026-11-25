import unreal
reg=unreal.AssetRegistryHelpers.get_asset_registry()
assets=reg.get_assets_by_class(unreal.TopLevelAssetPath('/Script/UMGEditor','WidgetBlueprint'),True)
print('WIDGETS',[a.package_name for a in assets][:60])
print('EDITORUTIL',[n for n in dir(unreal) if 'Blueprint' in n and ('Library' in n or 'Subsystem' in n)])
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/UI/WBP_Inventory');g=B.add_function_graph(bp,'OnPaint');print(B.read_graph_dsl(g))
for term in ['DrawBox','DrawText','MakeBrush','DrawLine','GetLocalSize','GetWidgetFromName']:
 print(term,list(B.find_node_types(g,term,[])))
