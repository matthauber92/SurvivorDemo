import unreal
from pathlib import Path
pc=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');ic=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionComponent')
for b,n in [(pc,'ServerMoveInventory'),(ic,'ServerInteract')]:
 f=unreal.find_object(b.generated_class(),n);print('FUNCTION',f)
 print('METHODS',[x for x in dir(f) if 'flag' in x or 'function' in x])
 for prop in ['FunctionFlags','function_flags']:
  try:print(prop,f.get_editor_property(prop))
  except Exception as e:print(str(e))
 t=unreal.AssetExportTask();t.object=f;t.filename=str(Path(unreal.Paths.project_saved_dir())/'InventoryDragValidation'/(n+'-function.t3d'));t.exporter=unreal.ObjectExporterT3D();t.automated=True;t.prompt=False;unreal.Exporter.run_asset_export_task(t)
print('PC_REPLICATES',unreal.get_default_object(pc.generated_class()).get_editor_property('replicates'))
