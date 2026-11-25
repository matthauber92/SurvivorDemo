import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');g=B.get_graph(b,'EventGraph')
for n in list(B.find_nodes(g)):
 if isinstance(n,unreal.K2Node_EnhancedInputAction) and not any(p.connected_pins for p in B._get_node_info(n).output_pins):B.delete_node(n)
B.compile_blueprint(b,warnings_as_errors=True);assert unreal.EditorAssetLibrary.save_loaded_asset(b)
print('CLEANED_ACTION_BINDING')
