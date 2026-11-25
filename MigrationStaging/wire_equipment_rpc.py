import unreal,toolset_registry
from editor_toolset.toolsets.blueprint import BlueprintTools as B,_BlueprintCache
b=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');g=B.get_graph(b,'EventGraph')
new=next(n for n in B.find_nodes(g) if isinstance(n,unreal.K2Node_CustomEvent) and 'ServerTransferWeapon' in B._get_node_info(n).type_id)
old=next(n for n in B.find_nodes(g) if isinstance(n,unreal.K2Node_CustomEvent) and 'EquipmentRequestSignature' in B._get_node_info(n).type_id)
with toolset_registry.tool_raising_exceptions():
 for p in B._get_node_info(old).output_pins:
  for target in list(p.connected_pins):
   B.break_pins(p.pin_id,target);B.connect_pins(next(q.pin_id for q in B._get_node_info(new).output_pins if q.name==p.name),target)
 B.delete_node(old);B.compile_blueprint(b,warnings_as_errors=True)
_BlueprintCache.invalidate(b)
assert unreal.EditorAssetLibrary.save_loaded_asset(b,only_if_is_dirty=False)
print('EQUIPMENT_RPC_WIRED')
