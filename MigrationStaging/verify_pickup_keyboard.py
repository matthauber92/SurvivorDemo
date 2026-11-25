import unreal,json
from pathlib import Path
root='/Game/AIExample/Items/'
ic=unreal.load_class(None,root+'BP_InventoryComponent.BP_InventoryComponent_C');pic=unreal.load_class(None,root+'BP_ItemPickup.BP_ItemPickup_C')
checks={}
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
    pawn=unreal.GameplayStatics.get_player_pawn(w,0)
    checks[('server' if pawn.has_authority() else 'client')+'_pickup_disappeared']=not any(abs(a.get_actor_location().x)<1 and abs(a.get_actor_location().y)<1 for a in unreal.GameplayStatics.get_all_actors_of_class(w,pic))
    if pawn.has_authority():pawn=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Pawn) if not p.is_locally_controlled())
    inv=pawn.get_controller().get_component_by_class(ic)
    checks[('server' if pawn.has_authority() else 'client')+'_owner_received_30_ammo']=inv.call_method('GetItemQuantity',(unreal.Name('Ammo.Handgun'),))==30
report={'method':'Windows E keydown/keyup in focused client viewport, without action injection','checks':checks,'passed':all(checks.values())}
(Path(unreal.Paths.project_saved_dir())/'PickupValidation/keyboard-result.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
