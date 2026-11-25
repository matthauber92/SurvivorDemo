import unreal,toolset_registry
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');g=B.get_graph(b,'CloseInventory')
with toolset_registry.tool_raising_exceptions():
 for node in list(B.find_nodes(g)):
  if 'SetFocusToGameViewport' in B._get_node_info(node).type_id:B.delete_node(node)
B.compile_blueprint(b,warnings_as_errors=True)
assert b.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE
assert unreal.EditorAssetLibrary.save_loaded_asset(b,only_if_is_dirty=False)
print('Controller-specific GameOnly input focus retained; global viewport focus removed')
