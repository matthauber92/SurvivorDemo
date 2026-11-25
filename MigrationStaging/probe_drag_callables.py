import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
p=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');u=unreal.load_asset('/Game/AIExample/UI/WBP_Inventory');v=unreal.load_asset('/Game/AIExample/UI/WBP_InventoryDragVisual')
print('EVENTS',[str(x) for x in B.list_events(p) if 'Server' in str(x)])
print('PCFUNCS',[str(x) for x in B.list_functions(p) if 'Server' in str(x)])
for b in [p,u,v]:
 g=B.get_graph(b,'EventGraph')
 print(b.get_name(),list(B.find_node_types(g,'MoveInventory',[])),list(B.find_node_types(g,'DragTitle',[])))
print('VGRAPH',B.read_graph_dsl(B.get_graph(v,'EventGraph')))
