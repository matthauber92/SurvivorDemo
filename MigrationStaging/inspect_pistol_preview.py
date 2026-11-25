import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);i=p.get_controller().get_editor_property('InventoryComponent');a=p.get_component_by_class(unreal.SkeletalMeshComponent).get_anim_instance()
print('STATE',list(i.get_editor_property('WeaponMagazines')),list(i.get_editor_property('Quantities')),i.get_editor_property('Reloading'),a.get_editor_property('PistolLayerWeight'))
g=B.get_graph(unreal.load_asset('/Game/AIExample/Combat/Animation/ABP_SurvivorCombat'),'AnimGraph')
print('GETTERS',[(n.get_name(),B._get_node_info(n).type_id) for n in B.find_nodes(g) if isinstance(n,unreal.K2Node_VariableGet)])
