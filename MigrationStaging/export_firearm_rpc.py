import unreal
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');g=B.get_graph(bp,'EventGraph');n=next(n for n in B.find_nodes(g) if isinstance(n,unreal.K2Node_CustomEvent) and 'ServerPistolAction' in B._get_node_info(n).type_id)
t=unreal.AssetExportTask();t.object=n;t.filename=str((Path(unreal.Paths.project_saved_dir())/'firearm-rpc-node.t3d').resolve());t.exporter=unreal.ObjectExporterT3D();t.automated=True;t.prompt=False;assert unreal.Exporter.run_asset_export_task(t)
