import unreal,ast
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B,_BlueprintCache
p=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');u=unreal.load_asset('/Game/AIExample/UI/WBP_Inventory')
g=B.add_function_graph(p,'RequestMoveInventory')
for n,t in [('SourceSlot','int'),('TargetSlot','int'),('ExpectedID','name'),('ExpectedQuantity','int'),('ExpectedLayoutVersion','int')]:B.add_function_param(g,n,t,True)
B.write_graph_dsl(g,'''(fn RequestMoveInventory (SourceSlot TargetSlot ExpectedID ExpectedQuantity ExpectedLayoutVersion)
 (if (and (Pawn|IsLocalController) (Variables|Default|GetInventoryOpen))
  (CallFunction|ServerMoveInventory :SourceSlot SourceSlot :TargetSlot TargetSlot :ExpectedID ExpectedID :ExpectedQuantity ExpectedQuantity :ExpectedLayoutVersion ExpectedLayoutVersion)))''')
B.compile_blueprint(p);_BlueprintCache.invalidate(u)
source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_inventory_drag_ui.py').read_text())
for n in ast.walk(source):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='write' and isinstance(n.args[1],ast.Constant) and n.args[1].value=='OnDrop':B.write_graph_dsl(B.get_graph(u,'OnDrop'),ast.literal_eval(n.args[2]).replace('Class|BPInventoryPlayerController|ServerMoveInventory','Class|BPInventoryPlayerController|RequestMoveInventory'))
for b in [p,u]:B.compile_blueprint(b,warnings_as_errors=True);assert unreal.EditorAssetLibrary.save_loaded_asset(b)
