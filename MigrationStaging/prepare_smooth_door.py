import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionTestDoor')
g=B.get_graph(bp,'EventGraph')
for term in ['RelativeRotation','SetActorTickEnabled','Clamp','Lerp']:
    print(term,list(B.find_node_types(g,term,[])))
