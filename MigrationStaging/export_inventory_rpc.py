import unreal
from pathlib import Path
b=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController')
t=unreal.AssetExportTask();t.object=b;t.filename=str(Path(unreal.Paths.project_saved_dir())/'InventoryDragValidation/controller.t3d');t.exporter=unreal.ObjectExporterT3D();t.automated=True;t.prompt=False;unreal.Exporter.run_asset_export_task(t)
