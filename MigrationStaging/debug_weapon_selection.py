import unreal,json,time,traceback
from pathlib import Path
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
sw=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority());cw=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
hpc=unreal.GameplayStatics.get_player_controller(sw,0);cpc=unreal.GameplayStatics.get_player_controller(cw,0)
rpc=next(p.get_controller() for p in unreal.GameplayStatics.get_all_actors_of_class(sw,unreal.Pawn) if not p.is_locally_controlled())
hi=hpc.get_editor_property('InventoryComponent');ci=cpc.get_editor_property('InventoryComponent');ri=rpc.get_editor_property('InventoryComponent')
rp=rpc.get_controlled_pawn();cp=cpc.get_controlled_pawn();hp=hpc.get_controlled_pawn()
import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
for bp,names in [('/Game/AIExample/Items/BP_InventoryComponent',['TrySelectWeapon','SyncWeaponPresentation']),('/Game/AIExample/Items/BP_InventoryPlayerController',['RequestSelectWeapon','EventGraph'])]:
 b=unreal.load_asset(bp)
 for n in names:print(n,B.read_graph_dsl(B.get_graph(b,n)))
print('STATE',[(x.get_name(),x.get_editor_property('ActiveWeaponInstance'),list(x.get_editor_property('EquipmentInstances')),x.get_editor_property('LayoutVersion')) for x in [ci,ri]])
print('DIRECT',ri.call_method('TrySelectWeapon',(2,list(ri.get_editor_property('EquipmentInstances'))[2],ri.get_editor_property('LayoutVersion'))))
print('AFTER',ri.get_editor_property('ActiveWeaponInstance'),rp.get_editor_property('PublicActiveSlot'))

