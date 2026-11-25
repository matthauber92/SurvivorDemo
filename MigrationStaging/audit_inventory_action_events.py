import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');g=B.get_graph(b,'EventGraph')
for n in B.find_nodes(g):
 if isinstance(n,unreal.K2Node_EnhancedInputAction):print('ACTION_NODE',n.get_name(),[(p.name,len(p.connected_pins)) for p in B._get_node_info(n).output_pins])
