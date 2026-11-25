import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
g=B.get_graph(unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter'),'EventGraph')
for t in ['GetAllActors','RandomFloatinRange','AddControllerPitch','GetPlayerCameraManager']:print(t,[x for x in B.find_node_types(g,t,[]) if 'Casting' not in x][:12])
