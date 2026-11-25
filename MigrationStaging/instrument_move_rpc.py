import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
p=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');g=B.get_graph(p,'EventGraph');e=next(n for n in B.find_nodes(g) if isinstance(n,unreal.K2Node_CustomEvent) and 'ServerMoveInventory' in B._get_node_info(n).type_id)
n=B.create_node(g,'Development|PrintString',unreal.IntPoint(300,1000));ni=B._get_node_info(n);ep=next(x for x in B._get_node_info(e).output_pins if x.name=='then');np=next(x for x in ni.input_pins if x.name=='execute');op=next(x for x in ni.output_pins if x.name=='then')
for target in list(ep.connected_pins):B.break_pins(ep.pin_id,target);B.connect_pins(op.pin_id,target)
B.connect_pins(ep.pin_id,np.pin_id);B.set_pin_value(next(x.pin_id for x in ni.input_pins if x.name=='InString'),'INVENTORY_MOVE_RPC_RECEIVED')
# Instrument the local wrapper separately to identify routing.
g=B.get_graph(p,'RequestMoveInventory');B.write_graph_dsl(g,'''(fn RequestMoveInventory (SourceSlot TargetSlot ExpectedID ExpectedQuantity ExpectedLayoutVersion)
 (Development|PrintString :InString "INVENTORY_REQUEST_ENTERED")
 (if (and (Pawn|IsLocalController) (Variables|Default|GetInventoryOpen))
  (Development|PrintString :InString "INVENTORY_REQUEST_LOCAL")
  (CallFunction|ServerMoveInventory :SourceSlot SourceSlot :TargetSlot TargetSlot :ExpectedID ExpectedID :ExpectedQuantity ExpectedQuantity :ExpectedLayoutVersion ExpectedLayoutVersion)))''')
B.compile_blueprint(p);unreal.EditorAssetLibrary.save_loaded_asset(p)
