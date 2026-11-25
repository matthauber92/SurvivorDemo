import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
pc=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');ui=unreal.load_asset('/Game/AIExample/UI/WBP_Inventory')
for b,terms in [(pc,['ShowMouse','SetIgnore','ToggleInventory']),(ui,['Equal(Key','Key|Equal','InputEventfromKeyEvent'])]:
 g=B.get_graph(b,'EventGraph')
 for term in terms:print(b.get_name(),term,list(B.find_node_types(g,term,[])))
for g in B.list_graphs(ui):
 for n in B.find_nodes(g):
  if isinstance(n,unreal.K2Node_ComponentBoundEvent):print('DELETE_OLD_EVENT',n);B.delete_node(n)
print('PINAPI',[n for n in dir(unreal.BlueprintGraphPinLibrary) if 'name' in n])
print('NODEINFO',B.get_node_infos(B.find_nodes(B.get_graph(pc,'EventGraph'))))
