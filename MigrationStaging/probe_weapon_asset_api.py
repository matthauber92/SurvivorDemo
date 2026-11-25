import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
print('MESH_API',[(n,[x for x in dir(getattr(unreal,n)) if any(q in x.lower() for q in ['static','convert','socket'])]) for n in ['SkeletalMeshEditorSubsystem','StaticMeshEditorSubsystem','EditorSkeletalMeshLibrary','EditorStaticMeshLibrary'] if hasattr(unreal,n)])
print('GEOMETRY',[(n,[x for x in dir(getattr(unreal,n)) if 'copy' in x.lower()]) for n in dir(unreal) if 'GeometryScript' in n and ('Asset' in n or 'MeshAsset' in n)])
bp=unreal.load_asset('/Game/AIExample/Combat/Animation/ABP_SurvivorCombat')
for g in B.list_graphs(bp):
 if g.get_name()=='AnimGraph':
  for node in B.find_nodes(g):
   info=B._get_node_info(node)
   if any(x in info.type_id for x in ['AimOffset','BlendSpace','Layered','Slot']):print('ANIM_NODE',info)
