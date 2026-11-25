import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP');g=B.get_graph(bp,'ShouldTurnInPlace')
print(B.find_node_types(g,'>',[]))
