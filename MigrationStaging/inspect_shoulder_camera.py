import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out=Path(unreal.Paths.project_saved_dir())/'ShoulderCamera';out.mkdir(exist_ok=True)
report={}
for path in ['/Game/Blueprints/SandboxCharacter_CMC','/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter']:
 bp=unreal.load_asset(path)
 report[path]={'graphs':[g.get_name() for g in B.list_graphs(bp)],'variables':str(B.list_variables(bp))}
 for g in B.list_graphs(bp):
  if 'camera' in g.get_name().lower():
   (out/(bp.get_name()+'-'+g.get_name()+'.txt')).write_text(B.read_graph_dsl(g))
(out/'inspection.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
