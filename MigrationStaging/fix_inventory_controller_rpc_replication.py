import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
p=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController')
unreal.get_default_object(p.generated_class()).set_editor_property('replicates',True)
unreal.get_default_object(p.generated_class()).set_editor_property('only_relevant_to_owner',True)
B.compile_blueprint(p);unreal.EditorAssetLibrary.save_loaded_asset(p)
