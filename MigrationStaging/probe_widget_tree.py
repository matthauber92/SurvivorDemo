import unreal,json
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/UI/WBP_Inventory')
print(unreal.ToolsetLibrary.get_object_properties(bp,['WidgetTree']))
tree=unreal.find_object(bp,'WidgetTree');print('TREE',tree)
root=unreal.new_object(unreal.CanvasPanel,outer=tree,name='InventoryRoot')
print('SET',unreal.ToolsetLibrary.set_object_properties(tree,json.dumps({'RootWidget':root.get_path_name()})))
print(unreal.ToolsetLibrary.get_object_properties(tree,['RootWidget']))
print('WIDGET', [n for n in dir(unreal.WidgetLibrary) if any(t in n for t in ['input','create','focus'])])
g=B.get_graph(bp,'EventGraph')
for t in ['Widget|SetText(Text)','Appearance|SetBrushfromTexture','UserInterface|CreateWidget','Input|SetInputModeGameAndUI','Input|SetInputModeGameOnly','UserInterface|Viewport|AddtoPlayerScreen']:
 try: print(t,[(p.name,p.type_id) for p in B.get_node_type_pins(g,t).input_pins])
 except Exception as e:print(e)
g=B.add_function_graph(bp,'OnKeyDown');print('KEYGRAPH',B.read_graph_dsl(g))
print('PROPS',unreal.ToolsetLibrary.list_struct_properties(unreal.UserWidget.static_class()))
B.compile_blueprint(bp);unreal.EditorAssetLibrary.save_loaded_asset(bp)
