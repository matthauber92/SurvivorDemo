import unreal,json,toolset_registry
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
R='/Game/AIExample/';out=Path(unreal.Paths.project_saved_dir())/'EquipmentValidation'
pc=unreal.load_asset(R+'Items/BP_InventoryPlayerController')
for node in list(B.find_nodes(B.get_graph(pc,'EventGraph'))):
 if isinstance(node,unreal.K2Node_CustomEvent) and 'EquipmentRequestSignature' in B._get_node_info(node).type_id:B.delete_node(node)
compiled={};assets=[]
for name in ['Items/PDA_ItemDefinition','Items/BP_InventoryComponent','Items/BP_InventoryPlayerController','Items/BP_ItemPickup','UI/WBP_Inventory','UI/BP_InventoryDragOperation','UI/WBP_InventoryDragVisual','UI/WBP_InventoryDragProxy','Interaction/BP_InteractionComponent','Interaction/BP_InteractionTestDoor']:
 bp=unreal.load_asset(R+name)
 with toolset_registry.tool_raising_exceptions():B.compile_blueprint(bp,warnings_as_errors=True)
 assert bp.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE,name
 assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 compiled[name]='Up to date, no compiler warnings'
 assets.append(unreal.EditorAssetLibrary.find_asset_data(R+name))
 (out/(bp.get_name()+'-final-graphs.json')).write_text(json.dumps({g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(bp)},indent=2))
for name in ['Items/DA_PistolItem','Items/DA_EquipmentTestLongGun','Interaction/IMC_SurvivorInteraction']:
 assert unreal.EditorAssetLibrary.save_asset(R+name,only_if_is_dirty=False)
 assets.append(unreal.EditorAssetLibrary.find_asset_data(R+name))
settings=unreal.ValidateAssetsSettings(validation_usecase=unreal.DataValidationUsecase.COMMANDLET,collect_per_asset_details=True)
ret,res=unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem).validate_assets_with_settings(assets,settings)
stats={k:res.get_editor_property(k) for k in ['num_requested','num_checked','num_valid','num_invalid','num_skipped','num_warnings','num_unable_to_validate']}
assert stats['num_invalid']==0 and stats['num_warnings']==0,stats
tests={n:json.loads((out/(n+'-result.json')).read_text()) for n in ['singleplayer','multiplayer','mouse']}
for n in ['singleplayer','multiplayer']:
 tests['pickup_door_'+n]=json.loads((Path(unreal.Paths.project_saved_dir())/'PickupValidation'/(n+'-result.json')).read_text())
assert all(t['passed'] for t in tests.values())
inv=unreal.get_default_object(unreal.load_asset(R+'Items/BP_InventoryComponent').generated_class())
assert list(inv.get_editor_property('EquipmentInstances'))==['','',''] and inv.get_editor_property('MaximumSlots')==8
assert unreal.get_default_object(pc.generated_class()).get_editor_property('only_relevant_to_owner')
report={'milestone':'5A','status':'implemented and validated','test_map':R+'Maps/Lvl_EquipmentTest','compiled_blueprints':compiled,'asset_validation':stats,'tests':tests,
 'controls':['I opens/closes inventory; Escape closes.','Select a backpack weapon, then click Primary, Secondary, or Sidearm.','Right-click equipment to unequip, or select it and click it again.','Select equipment then a compatible occupied backpack/equipment slot to swap.','Existing backpack drag-and-drop remains available.'],
 'architecture':['Same inventory component; equipment uses three independent instance references and does not count toward eight backpack slots.','Server validates locations, compatibility, expected instance and layout version before synchronous atomic transfer.','Stable GUID strings identify weapon records; magazine state stays in the record across transfers and swaps.','Inventory component belongs to an owner-relevant replicated PlayerController; other clients do not receive the private inventory.','Weapon state is preserved for the current session; disk save/load and public equipment representation are future work.'],
 'manual_verification_remaining':['14-player contention/load; only two-player listen-server PIE was tested.','Packaged/separate-process networking, latency, packet loss, reconnect and late join.','Human review of layout at other resolutions and final art; long gun uses a labeled placeholder mesh/icon.'],
 'scope':'No weapon attachment, aiming, firing, reloading, animations, source-project modifications or Git initialization.'}
(out/'milestone5a-report.json').write_text(json.dumps(report,indent=2));print('MILESTONE_5A_VALIDATED',stats)
