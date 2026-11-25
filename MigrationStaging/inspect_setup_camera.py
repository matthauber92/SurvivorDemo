import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools
bp = unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC')
graph = BlueprintTools.get_graph(bp, 'SetupCamera')
for node in BlueprintTools.find_nodes(graph):
    info = BlueprintTools._get_node_info(node)
    if 'PlayerController' in info.type_id:
        print(info)
