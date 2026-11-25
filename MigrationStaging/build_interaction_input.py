import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
root='/Game/AIExample/Interaction'
tools=unreal.AssetToolsHelpers.get_asset_tools()
def data(name,cls):
    if unreal.EditorAssetLibrary.does_asset_exist(root+'/'+name):return unreal.load_asset(root+'/'+name)
    f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',cls)
    return tools.create_asset(name,root,cls,f)
action=data('IA_SurvivorInteract',unreal.InputAction)
action.set_editor_property('value_type',unreal.InputActionValueType.BOOLEAN)
context=data('IMC_SurvivorInteraction',unreal.InputMappingContext)
context.unmap_all()
key=unreal.Key();key.import_text('E')
context.map_key(action,key)
unreal.EditorAssetLibrary.save_loaded_asset(action);unreal.EditorAssetLibrary.save_loaded_asset(context)
child=unreal.load_asset(root+'/BP_SurvivorInteractionCharacter')
g=B.add_function_graph(child,'SetupInteractionInput')
B.write_graph_dsl(g,'''(fn SetupInteractionInput ()
 (if (Pawn|IsLocallyControlled)
  (bind PC (Utilities|Casting|CastToPlayerController :Object (Pawn|GetController))
   (:then
    (Input|AddMappingContext
     :self (PlayerController|LocalPlayerSubsystems|GetEnhancedInputLocalPlayerSubsystem :PlayerController PC)
     :MappingContext "/Game/AIExample/Interaction/IMC_SurvivorInteraction.IMC_SurvivorInteraction"
     :Priority 1))
   (:CastFailed))))''')
# A timer tolerates possession/replication arriving after BeginPlay without replacing GASP events.
g=B.get_graph(child,'EventGraph')
print('Child events',B.read_graph_dsl(g))
print('Input event nodes',list(B.find_node_types(g,'IA_SurvivorInteract',[])))
print('Parent begin',list(B.find_node_types(g,'Parent:BeginPlay',[])))
print('Parent tick',list(B.find_node_types(g,'Parent:Tick',[])))
print('Component getter',list(B.find_node_types(g,'GetInteractionComponent',[])))
B.compile_blueprint(child);unreal.EditorAssetLibrary.save_loaded_asset(child)
f=unreal.BlueprintFactory();f.set_editor_property('parent_class',unreal.HUD)
hud=unreal.load_asset(root+'/BP_InteractionHUD') if unreal.EditorAssetLibrary.does_asset_exist(root+'/BP_InteractionHUD') else tools.create_asset('BP_InteractionHUD',root,unreal.Blueprint,f)
B.compile_blueprint(hud)
hg=B.get_graph(hud,'EventGraph')
data={}
for term in ['DrawHUD','DrawText','GetOwningPawn','ToString(Text)','GetComponentByClass','CastToBP_InteractionComponent','GetPromptText']:
    data[term]=list(B.find_node_types(hg,term,[]))
(Path(unreal.Paths.project_saved_dir())/'InteractionValidation/hud-nodes.json').write_text(json.dumps(data,indent=2))
print('Input assets saved')

