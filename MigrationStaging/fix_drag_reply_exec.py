import unreal,ast
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
ui=unreal.load_asset('/Game/AIExample/UI/WBP_Inventory')
source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_inventory_drag_ui.py').read_text())
for n in ast.walk(source):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='write' and isinstance(n.args[1],ast.Constant) and n.args[1].value=='OnPreviewMouseButtonDown':B.write_graph_dsl(B.get_graph(ui,'OnPreviewMouseButtonDown'),ast.literal_eval(n.args[2]))
for path in ['UI/WBP_Inventory','UI/WBP_InventoryDragVisual','UI/BP_InventoryDragOperation','Items/BP_InventoryPlayerController','Items/BP_InventoryComponent']:
 b=unreal.load_asset('/Game/AIExample/'+path);B.compile_blueprint(b,warnings_as_errors=True);print(path,b.get_editor_property('status'));assert b.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE;unreal.EditorAssetLibrary.save_loaded_asset(b)
