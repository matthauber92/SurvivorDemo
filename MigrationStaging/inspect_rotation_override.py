import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter')
g=B.get_graph(bp,'UpdateRotation_PreCMC')
print(B.read_graph_dsl(g));print(B.find_node_types(g,'UpdateRotation',[]))
p=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC')
for n in B.find_nodes(B.get_graph(p,'UpdateRotation_PreCMC')):
 print(B._get_node_info(n))
