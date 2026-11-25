import unreal,json
from editor_toolset.toolsets.blueprint import BlueprintTools as B,_BlueprintCache
b=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');g=B.get_graph(b,'EventGraph')
events=[n for n in B.find_nodes(g) if isinstance(n,unreal.K2Node_CustomEvent) and 'EquipmentRequestSignature' in B._get_node_info(n).type_id]
e=events[0]
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];pc=unreal.GameplayStatics.get_player_controller(w,0)
for prop,value in [('CustomFunctionName','ServerTransferWeapon'),('FunctionFlags','203555008')]:unreal.SystemLibrary.execute_console_command(w,'set '+e.get_path_name()+' '+prop+' '+value,pc)
print(B._get_node_info(e).type_id)
for extra in events[1:]:B.delete_node(extra)
B.compile_blueprint(b);_BlueprintCache.invalidate(b)
print(list(B.find_node_types(B.get_graph(b,'RequestEquipmentTransfer'),'ServerTransfer',[])))
unreal.EditorAssetLibrary.save_loaded_asset(b,only_if_is_dirty=False)
