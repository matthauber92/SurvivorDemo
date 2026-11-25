import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.object import ObjectTools as O
bp=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP')
n=next(n for n in B.find_nodes(B.get_graph(bp,'AnimGraph')) if 'OffsetRoot' in n.get_class().get_name())
print(O.get_properties(n,['node']))
print(B._get_node_info(n))
