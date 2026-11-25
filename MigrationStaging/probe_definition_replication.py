import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Items/BP_ItemPickup');g=B.get_graph(bp,'EventGraph')
for term in ['SoftObjectPath','SoftObjectReference','LoadAssetBlocking','GetPathName']:
 print(term,list(B.find_node_types(g,term,[])))
for t in ['Utilities|GetSoftObjectPath','Utilities|ToSoftObjectPath','Utilities|ToSoftObjectReference','Utilities|LoadAssetBlocking','Utilities|MakeSoftObjectPath','Utilities|ToString(SoftObjectReference)']:
 i=B.get_node_type_pins(g,t);print(t,[(p.name,p.type_id) for p in i.input_pins],[(p.name,p.type_id) for p in i.output_pins])
