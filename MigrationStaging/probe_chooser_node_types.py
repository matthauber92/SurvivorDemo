import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP');g=B.get_graph(bp,'Update_MotionMatching')
print(B.find_node_types(g,'Chooser'))
for n in B.find_nodes(g):
 if 'EvaluateChooser' in B._get_node_info(n).type_id:
  print('PROPERTIES',unreal.ToolsetLibrary.list_struct_properties(n.get_class()))
  print('NODE_METHODS',[a for a in dir(n) if any(s in a.lower() for s in ['recon','refresh','chooser'])])
