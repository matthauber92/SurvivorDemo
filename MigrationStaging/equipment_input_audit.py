import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');g=B.get_graph(b,'EventGraph')
for n in B.find_nodes(g):
 if isinstance(n,unreal.K2Node_EnhancedInputAction):print(str(B._get_node_info(n)))
print(B.read_graph_dsl(B.get_graph(b,'ToggleInventory')))
