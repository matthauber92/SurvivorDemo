import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter')
B.remove_function_graph(bp,'GetDesiredGait');g=B.add_function_graph(bp,'GetDesiredGait')
for n in B.find_nodes(g):print(B._get_node_info(n))
print('SELECT',B.find_node_types(g,'Select',[])[:30])
