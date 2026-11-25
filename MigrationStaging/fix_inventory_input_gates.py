import unreal,ast,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController')
source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_inventory_ui_logic.py').read_text())
for node in ast.walk(source):
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='write' and isinstance(node.args[1],ast.Constant) and node.args[1].value in ['CloseInventory','ToggleInventory']:
  s=ast.literal_eval(node.args[2]).replace('Input|SetIgnoreMoveInput true','Input|SetIgnoreMoveInput :bNewMoveInput true').replace('Input|SetIgnoreMoveInput false','Input|SetIgnoreMoveInput :bNewMoveInput false').replace('Input|SetIgnoreLookInput true','Input|SetIgnoreLookInput :bNewLookInput true').replace('Input|SetIgnoreLookInput false','Input|SetIgnoreLookInput :bNewLookInput false')
  B.write_graph_dsl(B.get_graph(b,node.args[1].value),s)
B.compile_blueprint(b);unreal.EditorAssetLibrary.save_loaded_asset(b)
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.LevelEditorPlaySettings'))
print('SET',unreal.ToolsetLibrary.set_object_properties(s,json.dumps({'playNetMode':'PIE_Standalone','playNumberOfClients':1,'runUnderOneProcess':True,'newWindowWidth':1280,'newWindowHeight':800})))
print(unreal.ToolsetLibrary.get_object_properties(s,['playNetMode','playNumberOfClients']))
