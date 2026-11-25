import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
def run():
    report={}
    for name in ['BP_InteractionComponent','BP_InteractionTestDoor','BP_SurvivorInteractionCharacter','BP_InteractionHUD']:
        bp=unreal.load_asset('/Game/AIExample/Interaction/'+name)
        report[name]={g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(bp)}
    (Path(unreal.Paths.project_saved_dir())/'InteractionValidation/graphs.json').write_text(json.dumps(report,indent=2))
    for name,gs in report.items():
        print(name,{k:len(v) for k,v in gs.items()})
run()
