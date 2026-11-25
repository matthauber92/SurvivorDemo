import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC');print('GRAPHS',[g.get_name() for g in B.list_graphs(b) if 'Input' in g.get_name()]);print('VARS',[x for x in B.list_variables(b) if 'Aim' in x or 'Input' in x])
for node in ['Animation|Blends|Layeredblendperbone','Animation|Sequences|SequencePlayer',"Animation|Montage|Slot'DefaultSlot'"]:
 a=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP');g=B.get_graph(a,'AnimGraph');info=B.get_node_type_pins(g,node);print('PINS',node,[(p.name,p.type_id,p.value) for p in info.input_pins],[(p.name,p.type_id) for p in info.output_pins])
