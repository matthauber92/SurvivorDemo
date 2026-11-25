import unreal,json
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.object import ObjectTools as O
bp=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController')
for name in ['RequestPistolAction','PistolAimStart']:print(name,B.read_graph_dsl(B.get_graph(bp,name)))
g=B.get_graph(bp,'EventGraph')
for n in B.find_nodes(g):
 if isinstance(n,unreal.K2Node_CustomEvent) and 'ServerPistolAction' in B._get_node_info(n).type_id:print('EVENT',B._get_node_info(n));print('PROPS',O.list_properties(n))
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False);cw=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority());cp=unreal.GameplayStatics.get_player_pawn(cw,0);cpc=cp.get_controller();ci=cpc.get_editor_property('InventoryComponent')
sw=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority());sp=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(sw,cp.get_class()) if not p.is_locally_controlled());si=sp.get_controller().get_editor_property('InventoryComponent')
print('INVENTORYOPEN',cpc.get_editor_property('InventoryOpen'))
print('SERVER_DIRECT_AIM',si.call_method('TryPistolAction',(1,si.get_editor_property('ActiveWeaponInstance'),sp.get_actor_location(),unreal.Vector(1,0,0))))
cpc.call_method('RequestPistolAction',(1,));print('AFTER',sp.get_editor_property('PublicAiming'),cp.get_editor_property('PublicAiming'))
