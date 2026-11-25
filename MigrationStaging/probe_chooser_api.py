import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
print('API',[(n,[v for v in dir(getattr(unreal,n)) if not v.startswith('_')]) for n in dir(unreal) if 'Chooser' in n and ('Library' in n or 'Subsystem' in n)])
bp=unreal.load_asset('/Game/AIExample/Combat/Animation/ABP_SurvivorCombat')
for g in B.list_graphs(bp):
 for n in B.find_nodes(g):
  info=B._get_node_info(n)
  if 'Chooser' in info.type_id:print('CHOOSER_NODE',g.get_name(),n.get_name(),info)
