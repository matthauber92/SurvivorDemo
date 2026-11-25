import unreal,ast
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
p=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');g=B.get_graph(p,'EventGraph')
for n in list(B.find_nodes(g)):
 info=B._get_node_info(n)
 if 'PrintString' in info.type_id:
  ip=next(x for x in info.input_pins if x.name=='execute');op=next(x for x in info.output_pins if x.name=='then')
  for a in list(ip.connected_pins):
   for b in list(op.connected_pins):B.connect_pins(a,b)
  B.delete_node(n)
B.write_graph_dsl(B.get_graph(p,'RequestMoveInventory'),'''(fn RequestMoveInventory (SourceSlot TargetSlot ExpectedID ExpectedQuantity ExpectedLayoutVersion)
 (if (and (Pawn|IsLocalController) (Variables|Default|GetInventoryOpen))
  (CallFunction|ServerMoveInventory :SourceSlot SourceSlot :TargetSlot TargetSlot :ExpectedID ExpectedID :ExpectedQuantity ExpectedQuantity :ExpectedLayoutVersion ExpectedLayoutVersion)))''')
# Ensure native RPC now connects directly to the authoritative mutation.
e=next(n for n in B.find_nodes(g) if isinstance(n,unreal.K2Node_CustomEvent) and 'ServerMoveInventory' in B._get_node_info(n).type_id)
call=next(n for n in B.find_nodes(g) if 'TryMoveSlot' in B._get_node_info(n).type_id)
B.connect_pins(next(x.pin_id for x in B._get_node_info(e).output_pins if x.name=='then'),next(x.pin_id for x in B._get_node_info(call).input_pins if x.name=='execute'))
B.compile_blueprint(p,warnings_as_errors=True);unreal.EditorAssetLibrary.save_loaded_asset(p)
