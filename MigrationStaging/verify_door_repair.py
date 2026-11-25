import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionTestDoor')
B.compile_blueprint(bp)
print('EDIT_API',[n for n in dir(unreal.BlueprintEditorLibrary) if 'mark' in n or 'refresh' in n])
task=unreal.AssetExportTask();task.object=bp;task.filename=unreal.Paths.project_saved_dir()+'InteractionValidation/door.t3d';task.exporter=unreal.ObjectExporterT3D();task.automated=True;task.prompt=False
unreal.Exporter.run_asset_export_task(task)
iface=unreal.load_asset('/Game/AIExample/Interaction/BPI_Interactable')
print('IMPLEMENTS',unreal.SystemLibrary.does_implement_interface(unreal.get_default_object(bp.generated_class()),iface.generated_class()))
unreal.EditorAssetLibrary.save_loaded_asset(bp)
print('GRAPH',B.read_graph_dsl(B.get_graph(bp,'TryInteract')))
