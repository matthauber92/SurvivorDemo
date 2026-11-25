import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC');result={}
print('GRAPHS',[g.get_name() for g in B.list_graphs(bp)])
for g in B.list_graphs(bp):
 if any(t in g.get_name().lower() for t in ['rotation','facing','turn','strafe']):result[g.get_name()]=B.read_graph_dsl(g)
(Path(unreal.Paths.project_saved_dir())/'parent-turning.json').write_text(json.dumps(result,indent=2))
