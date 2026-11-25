import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A
root='/Game/AIExample/Items/'
for name,props in [('BP_PickupTestGameMode',['player_controller_class','default_pawn_class','hud_class']),('BP_InventoryComponent',['MaximumSlots','replicates']),('BP_ItemPickup',['Quantity','ItemDefinition','replicates'])]:
    bp=unreal.load_asset(root+name)
    print(name,{p:str(unreal.get_default_object(bp.generated_class()).get_editor_property(p)) for p in props})
    B.compile_blueprint(bp)
    print('AFTER_COMPILE',{p:str(unreal.get_default_object(bp.generated_class()).get_editor_property(p)) for p in props})
    unreal.EditorAssetLibrary.save_loaded_asset(bp)
pc=unreal.load_asset(root+'BP_InventoryPlayerController')
print('CONTROLLER_COMPONENTS',[(c.get_name(),c.get_editor_property('replicates')) for c in A.get_components(unreal.get_default_object(pc.generated_class()))])
