import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionHUD')
print('HUD_GRAPH',B.read_graph_dsl(B.get_graph(bp,'EventGraph')))
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
    pc=unreal.GameplayStatics.get_player_controller(w,0)
    if not pc.has_authority():
        unreal.SystemLibrary.execute_console_command(w,'Shot SHOWUI',pc)

