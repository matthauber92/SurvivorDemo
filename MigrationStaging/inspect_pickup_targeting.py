import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A
for path in ['Items/BP_ItemPickup','Interaction/BP_InteractionComponent']:
 b=unreal.load_asset('/Game/AIExample/'+path)
 print(path,{g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(b)})
 for c in A.get_components(unreal.get_default_object(b.generated_class())):print('COMP',c.get_name(),c.get_class().get_name())
