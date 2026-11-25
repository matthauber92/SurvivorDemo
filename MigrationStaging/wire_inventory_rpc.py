import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');g=B.get_graph(b,'EventGraph')
print([(n.get_name(),B._get_node_info(n).type_id) for n in B.find_nodes(g) if isinstance(n,unreal.K2Node_CustomEvent)])
e=next(n for n in B.find_nodes(g) if isinstance(n,unreal.K2Node_CustomEvent) and 'ServerMoveInventory' in B._get_node_info(n).type_id)
old=next(n for n in B.find_nodes(g) if isinstance(n,unreal.K2Node_CustomEvent) and 'MoveSlotSignature' in B._get_node_info(n).type_id)
oldinfo=B._get_node_info(old);newinfo=B._get_node_info(e)
for p in oldinfo.output_pins:
 for target in list(p.connected_pins):
  B.break_pins(p.pin_id,target);B.connect_pins(next(q.pin_id for q in newinfo.output_pins if q.name==p.name),target)
B.delete_node(old);B.compile_blueprint(b,warnings_as_errors=True);unreal.EditorAssetLibrary.save_loaded_asset(b)
print('SERVER_RPC_WIRED')
