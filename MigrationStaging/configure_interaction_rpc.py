import unreal
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionComponent')
event=next(n for n in B.find_nodes(B.get_graph(bp,'EventGraph')) if isinstance(n,unreal.K2Node_CustomEvent))
asset=unreal.ConsoleVariablesAsset()
print(unreal.ConsoleVariablesEditorAssetSaveData.__doc__)
data=unreal.ConsoleVariablesEditorAssetSaveData()
data.set_editor_property('command_name','set '+event.get_path_name()+' FunctionFlags')
data.set_editor_property('command_value','203555008')
asset.add_or_set_console_object_saved_data(data)
asset.execute_saved_commands(unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world())
B.compile_blueprint(bp)
t=unreal.AssetExportTask();t.object=bp;t.filename=str(Path(unreal.Paths.project_saved_dir())/'InteractionValidation/component.t3d');t.exporter=unreal.ObjectExporterT3D();t.automated=True;t.prompt=False
unreal.Exporter.run_asset_export_task(t)
