import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionTestDoor')
for name in ['GetInteractionPrompt','TryInteract']:
    B.remove_function_graph(bp,name)
B.compile_blueprint(bp)
unreal.BlueprintEditorLibrary.refresh_open_editors_for_blueprint(bp)
