import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out=Path(unreal.Paths.project_saved_dir())/'PickupValidation';out.mkdir(exist_ok=True)
report={}
for name in ['BPI_Interactable','BP_InteractionComponent','BP_SurvivorInteractionCharacter','BP_InteractionTestGameMode','BP_InteractionTestDoor']:
    bp=unreal.load_asset('/Game/AIExample/Interaction/'+name)
    report[name]={g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(bp)}
gm=unreal.get_default_object(unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionTestGameMode').generated_class())
report['controller']=gm.get_editor_property('player_controller_class').get_path_name()
report['struct_api']=[n for n in dir(unreal) if any(s in n for s in ['Structure','StructEditor','UserDefinedStruct'])]
report['blueprint_api']=[n for n in dir(unreal.BlueprintEditorLibrary) if any(s in n for s in ['replic','struct','interface'])]
(out/'architecture-before.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k in ['controller','struct_api','blueprint_api']}))
print('STRUCT_FACTORY',getattr(unreal,'StructureFactory',None))
print('DATA',unreal.PrimaryDataAsset)
