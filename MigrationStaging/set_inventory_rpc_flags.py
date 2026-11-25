import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');e=next(n for n in B.find_nodes(B.get_graph(b,'EventGraph')) if isinstance(n,unreal.K2Node_CustomEvent))
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];pc=unreal.GameplayStatics.get_player_controller(w,0)
for prop,value in [('CustomFunctionName','ServerMoveInventory'),('FunctionFlags','203555008')]:unreal.SystemLibrary.execute_console_command(w,'set '+e.get_path_name()+' '+prop+' '+value,pc)
print('RPC',B._get_node_info(e).type_id)
