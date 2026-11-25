import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
print('GRAPH_METHODS',[x for x in dir(unreal.BlueprintGraphEditor) if any(k in x for k in ['node','pin'])])
for cls,methods in [(unreal.IKRigController,['set_skeletal_mesh','apply_auto_generated_retarget_definition','apply_auto_fbik']),(unreal.IKRetargeterController,['set_ik_rig','auto_map_chains','auto_align_all_bones','add_default_ops']),(unreal.IKRetargetBatchOperation,['run_batch_retarget'])]:
 for m in methods:
  if hasattr(cls,m):print(m,getattr(cls,m).__doc__)
print('INPUTS',unreal.IKRetargetBatchOperationInputs.__doc__)
b=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP');g=B.get_graph(b,'AnimGraph')
for term in ['Layered','Slot','SequencePlayer']:
 print('ANIM_TYPES',term,[x for x in B.find_node_types(g,term,[]) if 'Casting' not in x and 'Struct' not in x])
