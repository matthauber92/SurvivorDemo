import unreal
print('ENGINE_TYPES',dir(unreal.EngineTypes) if hasattr(unreal,'EngineTypes') else 'none')
print('CONVERT',[n for n in dir(unreal.SystemLibrary) if 'trace_type' in n or 'collision_channel' in n])
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Items/BP_ItemPickup');g=B.get_graph(bp,'ApplyDefinitionMesh')
for t in ['SetCollisionResponseToChannel','SetCanEverAffectNavigation']:print(t,list(B.find_node_types(g,t,[])))
for n in unreal.ObjectIterator(unreal.AnimGraphNode_Base):
 if 'FootPlacement' in n.get_class().get_name():
  try:print('FOOT',n.get_path_name(),n.get_editor_property('node').export_text())
  except Exception as e:print(e)
