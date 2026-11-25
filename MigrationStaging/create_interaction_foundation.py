import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
root='/Game/AIExample/Interaction'
def create(name,cls=None,interface=False):
    path=root+'/'+name
    if unreal.EditorAssetLibrary.does_asset_exist(path): return unreal.load_asset(path)
    f=unreal.BlueprintInterfaceFactory() if interface else unreal.BlueprintFactory()
    if cls:f.set_editor_property('parent_class',cls)
    a=unreal.AssetToolsHelpers.get_asset_tools().create_asset(name,root,unreal.Blueprint,f)
    assert a
    return a
bpi=create('BPI_Interactable',interface=True)
for name in ['GetInteractionPrompt','TryInteract']:
    g=B.add_function_graph(bpi,name)
    B.add_object_function_param(g,'Interactor',unreal.Pawn.static_class(),True)
    B.add_function_param(g,'Prompt' if name.startswith('Get') else 'Accepted','text' if name.startswith('Get') else 'bool',False)
B.compile_blueprint(bpi)
unreal.EditorAssetLibrary.save_loaded_asset(bpi)
comp=create('BP_InteractionComponent',unreal.ActorComponent)
event=B.add_event(comp,'ServerInteract')
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
unreal.SystemLibrary.execute_console_command(world,'set '+event.get_path_name()+' FunctionFlags 203555008')
B.compile_blueprint(comp)
unreal.EditorAssetLibrary.save_loaded_asset(comp)
task=unreal.AssetExportTask()
task.object=comp
task.filename=str(Path(unreal.Paths.project_saved_dir())/'InteractionValidation/component.t3d')
task.exporter=unreal.ObjectExporterT3D()
task.automated=True
task.prompt=False
unreal.Exporter.run_asset_export_task(task)
print('Foundation created', event.get_path_name())
