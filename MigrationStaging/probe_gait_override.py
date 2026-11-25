import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter')
g=B.add_function_graph(bp,'GetDesiredGait')
print('NODES',[(B._get_node_info(n).type_id,[(p.name,p.value,p.type_id) for p in B._get_node_info(n).input_pins]) for n in B.find_nodes(g)])
print('TYPES',B.find_node_types(g,'GetDesiredGait',[]))
