import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
for path in ['/Game/Blueprints/SandboxCharacter_CMC_ABP','/Game/AIExample/Combat/Animation/ABP_SurvivorCombat','/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter']:
 bp=unreal.load_asset(path);print(path,bp.get_editor_property('status'))
 if 'Character' in bp.get_name() and 'Interaction' in bp.get_name():print(B.read_graph_dsl(B.get_graph(bp,'InitializePistolAnimation')))
c=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/CHT_PoseSearchDatabases');print('CONTEXT',c.get_editor_property('context_data')[0].export_text())
print('PIE',unreal.EditorLevelLibrary.get_pie_worlds(False))
