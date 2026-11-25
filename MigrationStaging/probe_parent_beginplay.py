import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter');g=B.get_graph(b,'EventGraph')
print('BEGIN_NODES',[(n.get_name(),B._get_node_info(n).type_id) for n in B.find_nodes(g) if 'BeginPlay' in B._get_node_info(n).type_id or isinstance(n,unreal.K2Node_CallParentFunction)])
print('PARENT_TYPES',list(B.find_node_types(g,'BeginPlay',[])))
