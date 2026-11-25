import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out={}
for path in ['/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter','/Game/AIExample/Combat/Animation/ABP_SurvivorCombat','/Game/Blueprints/SandboxCharacter_CMC']:
 bp=unreal.load_asset(path)
 if not bp:continue
 out[path]={}
 for g in B.list_graphs(bp):
  name=g.get_name()
  if any(s in name.lower() for s in ['gait','speed','pistollayer','hipfire','shouldercamera','aim']):out[path][name]=B.read_graph_dsl(g)
 out[path]['graphs']=[g.get_name() for g in B.list_graphs(bp)]
Path(unreal.Paths.project_saved_dir(),'pistol-movement-inspect.json').write_text(json.dumps(out,indent=2))
