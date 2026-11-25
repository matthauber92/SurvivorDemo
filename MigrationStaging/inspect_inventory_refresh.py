import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
for path,names in [('Items/BP_InventoryComponent',['TryAddItem','NotifyInventoryChanged']),('Items/BP_InventoryPlayerController',['RefreshInventory']),('UI/WBP_Inventory',['RefreshInventory'])]:
 b=unreal.load_asset('/Game/AIExample/'+path)
 for n in names:print(n,B.read_graph_dsl(B.get_graph(b,n)))
