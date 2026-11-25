import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
g=B.get_graph(unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController'),'EventGraph')
for t in B.find_node_types(g,'GetPlayerCameraManager',[]):
 print(t,[(p.name,p.type_id) for p in B.get_node_type_pins(g,t).input_pins])
