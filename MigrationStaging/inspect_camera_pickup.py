import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out={}
for rel in ['Interaction/BP_InteractionComponent','Items/BP_ItemPickup','Interaction/BP_SurvivorInteractionCharacter']:
 b=unreal.load_asset('/Game/AIExample/'+rel)
 names={'BP_InteractionComponent':['UpdateFocus','ValidateTarget','RequestInteraction','EventGraph'],'BP_ItemPickup':['TryInteract','GetInteractionPrompt','UserConstructionScript'],'BP_SurvivorInteractionCharacter':['UpdateShoulderCamera']}[b.get_name()]
 out[rel]={n:B.read_graph_dsl(B.get_graph(b,n)) for n in names}
 d=B.get_default_object(b)
 out[rel]['defaults']={n:str(d.get_editor_property(n)) for n in B.list_variables(b) if 'Camera' in n or n in ['InteractionRange','Quantity','Claimed']}
p=Path(unreal.Paths.project_saved_dir())/'camera-pickup-inspect.json';p.write_text(json.dumps(out,indent=2));print(str(p))
