import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
for cl in ['IKRetargetBatchOperation','IKRigController','IKRetargeterController','AnimationLibrary','AnimationBlueprintLibrary','AnimSequence','AnimMontageFactory']:
 c=getattr(unreal,cl,None);print('TYPE',cl,[x for x in dir(c) if any(k in x for k in ['retarget','auto','skeleton','notify','bone','slot','track'])] if c else None)
 if cl=='IKRetargetBatchOperation' and c:print(c.duplicate_and_retarget.__doc__)
b=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP');g=B.get_graph(b,'AnimGraph')
for term in ['Layered','Slot','SequencePlayer','BlendSpace','ModifyBone']:
 print('NODE_TYPES',term,list(B.find_node_types(g,term,[]))[:15])
for n in B.find_nodes(g):
 if isinstance(n,unreal.AnimGraphNode_Root):print('ROOT',[(p.name,p.type_id,[str(c) for c in p.connected_pins]) for p in B._get_node_info(n).input_pins])
print('ANIMEVENT',B.read_graph_dsl(B.get_graph(b,'EventGraph')))
