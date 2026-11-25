import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A
root='/Game/AIExample/Interaction'
def bp(name,parent):
    existing=unreal.load_asset(root+'/'+name)
    if existing:return existing
    f=unreal.BlueprintFactory();f.set_editor_property('parent_class',parent)
    return unreal.AssetToolsHelpers.get_asset_tools().create_asset(name,root,unreal.Blueprint,f)
door=bp('BP_InteractionTestDoor',unreal.Actor)
if 'IsOpen' not in B.list_variables(door):
    B.add_variable(door,'IsOpen','bool')
    B.set_variable_replication(door,'IsOpen',unreal.BlueprintVariableReplication.REP_NOTIFY)
    B.add_variable(door,'NextInteractionTime','float')
    hinge=A.add_component(door,unreal.SceneComponent.static_class(),'DoorHinge')
    mesh=A.add_component(hinge,unreal.StaticMeshComponent.static_class(),'DoorPanel')
    mesh.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'))
    mesh.set_editor_property('relative_location',unreal.Vector(0,60,110))
    mesh.set_editor_property('relative_scale3d',unreal.Vector(.15,1.2,2.2))
    mesh.set_collision_profile_name('BlockAll')
B.compile_blueprint(door)
unreal.get_default_object(door.generated_class()).set_editor_property('replicates',True)
unreal.EditorAssetLibrary.save_loaded_asset(door)
component=unreal.load_asset(root+'/BP_InteractionComponent')
if 'InteractionRange' not in B.list_variables(component):
    B.add_variable(component,'InteractionRange','float')
    B.add_object_variable(component,'FocusedActor',unreal.Actor.static_class())
    B.add_object_variable(component,'OwnerPawn',unreal.Pawn.static_class())
    B.add_variable(component,'PromptText','text')
B.compile_blueprint(component)
cdo=unreal.get_default_object(component.generated_class())
cdo.set_editor_property('InteractionRange',250.0)
cdo.set_editor_property('replicates',True)
unreal.EditorAssetLibrary.save_loaded_asset(component)
child=bp('BP_SurvivorInteractionCharacter',unreal.load_asset('/Game/AIExample/Gameplay/Characters/BP_SurvivorCharacter').generated_class())
if not any(c.get_name().startswith('InteractionComponent') for c in A.get_components(unreal.get_default_object(child.generated_class()))):
    A.add_component(child,component.generated_class(),'InteractionComponent')
B.compile_blueprint(child);unreal.EditorAssetLibrary.save_loaded_asset(child)
gm=bp('BP_InteractionTestGameMode',unreal.GameModeBase)
B.compile_blueprint(gm)
unreal.get_default_object(gm.generated_class()).set_editor_property('default_pawn_class',child.generated_class())
unreal.EditorAssetLibrary.save_loaded_asset(gm)
data={}
for asset in [component,door,child]:
    graph=B.get_graph(asset,'EventGraph')
    data[asset.get_name()]={}
    for term in ['LineTrace','GetActorEyes','GetWorldLocation','GetPlayerCamera','GetControlRotation','GetController','GetOwner','IsLocallyControlled','DoesImplement','TryInteract','GetInteractionPrompt','SetRelativeRotation','GetDoorHinge','ServerInteract','GetEnhancedInput','AddMappingContext','IA_Interact','CreateWidget','DrawText']:
        data[asset.get_name()][term]=list(B.find_node_types(graph,term,[]))
(Path(unreal.Paths.project_saved_dir())/'InteractionValidation/node-types.json').write_text(json.dumps(data,indent=2))
print('Assets and node inventory saved')
