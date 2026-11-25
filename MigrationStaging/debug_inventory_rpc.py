import unreal
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionComponent');t=unreal.AssetExportTask();t.object=b;t.filename=str(Path(unreal.Paths.project_saved_dir())/'InventoryDragValidation/interaction.t3d');t.exporter=unreal.ObjectExporterT3D();t.automated=True;t.prompt=False;unreal.Exporter.run_asset_export_task(t)
b=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');print(B.read_graph_dsl(B.get_graph(b,'EventGraph')));print(B.read_graph_dsl(B.get_graph(b,'RequestMoveInventory')))
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
 p=unreal.GameplayStatics.get_player_controller(w,0)
 print('PC',p.has_authority(),p.get_editor_property('InventoryOpen'))
 if p.has_authority():
  other=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PlayerController) if a!=p);print('SERVER_DATA',other.get_editor_property('InventoryComponent').get_editor_property('Quantities'))
  other.call_method('ServerMoveInventory',(0,6,unreal.Name('Medical.FirstAidKit'),3,0));print('DIRECT_SERVER',other.get_editor_property('InventoryComponent').get_editor_property('SlotOrder'))
