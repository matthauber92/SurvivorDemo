import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP');g=B.get_graph(bp,'ShouldTurnInPlace')
for n in B.find_nodes(g):
 i=B._get_node_info(n);print(i.type_id,[(p.name,p.value,len(p.connected_pins)) for p in i.input_pins])
