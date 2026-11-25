import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter');g=B.get_graph(b,'EventGraph')
for t in ['Utilities|Struct|MakeSPlayerInputState','Utilities|Struct|BreakSPlayerInputState']:
 q=B.get_node_type_pins(g,t);print('PINS',t,[(p.name,p.type_id) for p in q.input_pins],[(p.name,p.type_id) for p in q.output_pins])
