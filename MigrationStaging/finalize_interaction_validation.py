import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A
root='/Game/AIExample/Interaction/'
folder=Path(unreal.Paths.project_saved_dir())/'InteractionValidation'
report=json.loads((folder/'play-result.json').read_text())
compiled={}
for name in ['BPI_Interactable','BP_InteractionComponent','BP_InteractionTestDoor','BP_SurvivorInteractionCharacter','BP_InteractionHUD','BP_InteractionTestGameMode']:
    bp=unreal.load_asset(root+name)
    B.compile_blueprint(bp)
    compiled[name]=str(bp.get_editor_property('status'))
    unreal.EditorAssetLibrary.save_loaded_asset(bp)
component=unreal.load_asset(root+'BP_InteractionComponent')
child=unreal.load_asset(root+'BP_SurvivorInteractionCharacter')
report['checks']['saved_component_replication']=unreal.get_default_object(component.generated_class()).get_editor_property('replicates') and all(c.get_editor_property('replicates') for c in A.get_components(unreal.get_default_object(child.generated_class())) if c.get_class()==component.generated_class())
door=unreal.load_asset(root+'BP_InteractionTestDoor')
report['checks']['saved_door_interface']=unreal.SystemLibrary.does_implement_interface(unreal.get_default_object(door.generated_class()),unreal.load_asset(root+'BPI_Interactable').generated_class())
hud=unreal.load_asset(root+'BP_InteractionHUD')
report['checks']['hud_draw_event_connected']='HUD|DrawText' in B.read_graph_dsl(B.get_graph(hud,'EventGraph'))
report['checks']['all_blueprints_compile']=all('BS_UP_TO_DATE' in s for s in compiled.values())
report['checks']['door_visual_callback_connected']='SetRelativeRotation' in B.read_graph_dsl(B.get_graph(door,'OnRep_IsOpen'))
report['validation_method']='Enhanced Input action injection in host/client PIE; live replicated state and hinge rotation checks; authoritative range, sight, origin and cooldown checks.'
report['passed']=all(report['checks'].values())
(folder/'play-result.json').write_text(json.dumps(report,indent=2))
(folder/'compile-result.json').write_text(json.dumps(compiled,indent=2))
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
print(json.dumps(report))
