import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
at=unreal.AssetToolsHelpers.get_asset_tools()
bp=unreal.load_asset('/Game/AIExample/UI/WBP_Inventory')
if not bp:
 f=unreal.WidgetBlueprintFactory();f.set_editor_property('parent_class',unreal.UserWidget)
 bp=at.create_asset('WBP_Inventory','/Game/AIExample/UI',unreal.WidgetBlueprint,f)
for p in ['WidgetTree','widget_tree']:
 try:
  tree=bp.get_editor_property(p);print('TREE',tree)
  root=unreal.new_object(unreal.CanvasPanel,outer=tree,name='InventoryRoot')
  tree.set_editor_property('RootWidget',root);print('ROOT_OK')
  break
 except Exception as e:print(e)
g=B.get_graph(bp,'EventGraph')
for term in ['SetInputMode','CreateWidget','AddtoPlayer','GetOwningPlayer','SetKeyboardFocus','SetUserFocus','GetKey','Handled','GetInventoryComponent','SetShowMouse','OnKeyDown','SetText','SetBrushFromTexture']:
 print(term,list(B.find_node_types(g,term,[])))
print('UMG', [n for n in dir(unreal) if 'WidgetLibrary' in n or 'WidgetBlueprintLibrary' in n])
B.compile_blueprint(bp);unreal.EditorAssetLibrary.save_loaded_asset(bp)
