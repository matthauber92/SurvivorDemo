import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionTestDoor')
B.compile_blueprint(bp)
assert 'BS_UP_TO_DATE' in str(bp.get_editor_property('status'))
assert abs(unreal.get_default_object(bp.generated_class()).get_editor_property('SwingDuration')-0.6)<0.001
unreal.EditorAssetLibrary.save_loaded_asset(bp)
print('COMPILED_AND_SAVED_SMOOTH_DOOR')
