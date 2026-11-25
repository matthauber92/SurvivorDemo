import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionComponent')
unreal.get_default_object(bp.generated_class()).set_editor_property('replicates',True)
unreal.EditorAssetLibrary.save_loaded_asset(bp)
child=unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter')
for c in A.get_components(unreal.get_default_object(child.generated_class())):
    if c.get_class()==bp.generated_class():
        print('TEMPLATE',c.get_path_name(),c.get_editor_property('replicates'))
        c.set_editor_property('replicates',True)
B.compile_blueprint(child)
unreal.EditorAssetLibrary.save_loaded_asset(child)
print('DEFAULT',unreal.get_default_object(bp.generated_class()).get_editor_property('replicates'))

