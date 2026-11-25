import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/UI/WBP_Inventory');g=B.get_graph(b,'OnKeyDown')
print('OPS',list(B.find_node_types(g,'==',[])))
