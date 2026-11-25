import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController')
for n in ['ToggleInventory','CloseInventory']:print(n,B.read_graph_dsl(B.get_graph(b,n)))
