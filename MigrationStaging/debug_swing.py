import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionTestDoor')
print(B.read_graph_dsl(B.get_graph(bp,'EventGraph')))
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
    d=unreal.GameplayStatics.get_all_actors_of_class(w,bp.generated_class())[0]
    print('SWING',d.has_authority(),[(p,d.get_editor_property(p)) for p in ['AnimationStartYaw','AnimationElapsed','SwingDuration','IsOpen']],d.is_actor_tick_enabled())
