import unreal,ast
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Items/BP_InventoryComponent')
source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_inventory_logic.py').read_text())
for node in ast.walk(source):
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='write' and ast.literal_eval(node.args[0])=='TryAddItem':
  s=ast.literal_eval(node.args[1]).replace('(return true)','(CallFunction|NotifyInventoryChanged) (return true)');B.write_graph_dsl(B.get_graph(b,'TryAddItem'),s)
B.compile_blueprint(b);unreal.EditorAssetLibrary.save_loaded_asset(b)
print('HAS_NOTIFY', 'NotifyInventoryChanged' in B.read_graph_dsl(B.get_graph(b,'TryAddItem')))
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.LevelEditorPlaySettings'))
for p,v in [('PlayNumberOfClients',1),('PlayNetMode',0),('RunUnderOneProcess',True),('NewWindowWidth',1280),('NewWindowHeight',800)]:s.set_editor_property(p,v)
print('SETTINGS')
