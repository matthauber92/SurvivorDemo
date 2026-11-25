import unreal,json
from editor_toolset.toolsets.blueprint import BlueprintTools as B
for path in ['/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter','/Game/Blueprints/CBP_SandboxCharacter','/Game/Blueprints/CBP_SandboxCharacter_CMC']:
 bp=unreal.load_asset(path)
 if not bp:continue
 print('BP',path)
 for g in B.list_graphs(bp):
  for n in B.find_nodes(g):
   info=B._get_node_info(n)
   if any(s in info.type_id for s in ['SetAnimInstance','InitializePistolAnimation','SetSkeletalMesh','UpdatePistolLayer']):print(g.get_name(),info)
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter')
print('EVENT',B.read_graph_dsl(B.get_graph(bp,'EventGraph')))
print('DEFAULT_ANIM',B.get_default_object(bp).mesh.get_editor_property('anim_class'))
