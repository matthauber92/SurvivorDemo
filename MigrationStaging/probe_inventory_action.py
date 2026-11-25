import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
c=unreal.load_asset('/Game/AIExample/Interaction/IMC_SurvivorInteraction');print('MAPPINGS',[m.export_text() for m in c.get_editor_property('default_key_mappings').get_editor_property('mappings')])
p=unreal.GameplayStatics.get_player_controller(unreal.EditorLevelLibrary.get_pie_worlds(False)[0],0)
for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem):
 if 'Transient' in s.get_path_name():s.inject_input_vector_for_action(unreal.load_asset('/Game/AIExample/UI/IA_ToggleInventory'),unreal.Vector(1,0,0),[],[])
