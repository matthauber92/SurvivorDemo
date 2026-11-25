import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
g=B.get_graph(unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController'),'RequestEquipmentTransfer')
for term in ['Equal','RegisterWeapon','ServerTransferWeapon']:
 print(term,[x for x in B.find_node_types(g,term,[]) if 'String' in x or 'Name)' in x or term!='Equal'])
print('server',list(B.find_node_types(g,'Server',[])))
print(B.read_graph_dsl(B.get_graph(unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController'),'EventGraph')))
