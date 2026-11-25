import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out=Path(unreal.Paths.project_saved_dir())/'InventoryDragValidation';compiled={}
for path in ['UI/WBP_Inventory','UI/WBP_InventoryDragVisual','UI/BP_InventoryDragOperation','Items/BP_InventoryPlayerController','Items/BP_InventoryComponent']:
 b=unreal.load_asset('/Game/AIExample/'+path);B.compile_blueprint(b,warnings_as_errors=True)
 assert b.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE,(path,b.get_editor_property('status'))
 assert unreal.EditorAssetLibrary.save_loaded_asset(b);compiled[path]='Up to date; no warnings'
 (out/(b.get_name()+'-graphs.json')).write_text(json.dumps({g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(b)},indent=2))
tests={n:json.loads((out/(n+'-result.json')).read_text()) for n in ['multiplayer','mouse','standalone-mouse']}
assert all(t['passed'] for t in tests.values())
regression=json.loads((Path(unreal.Paths.project_saved_dir())/'PickupValidation/multiplayer-result.json').read_text());assert regression['passed']
pc=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');inv=unreal.load_asset('/Game/AIExample/Items/BP_InventoryComponent')
assert all(B.get_variable_replication(pc,n)==unreal.BlueprintVariableReplication.NONE for n in ['InventoryWidget','InventoryOpen'])
assert unreal.get_default_object(pc.generated_class()).get_editor_property('only_relevant_to_owner')
assert sorted(list(unreal.get_default_object(inv.generated_class()).get_editor_property('SlotOrder')))==list(range(8))
report={
 'status':'Implemented and validated in standalone PIE and two-player PIE',
 'behavior':['Left-drag an occupied inventory slot to move its complete stack to an empty slot.','Drop on an occupied slot to swap positions. Quantities remain unchanged.','The drag ghost shows item icon, name, and quantity; the source dims while dragging.','Drop outside the grid to cancel. Empty slots cannot begin a drag.','Slot arrangement survives closing and reopening inventory during the session.'],
 'architecture':['Existing ItemIDs/Quantities storage and pickup capacity logic are unchanged.','A replicated eight-entry SlotOrder permutation on the same inventory component maps display slots to existing stack indices. No second inventory is created.','The owning controller sends a reliable ServerMoveInventory RPC. The server validates indices, occupied source, item ID, quantity, and layout version before swapping the order entries.','Stale or invalid requests do not change items or layout. Owner replication and RepNotify refresh only the owning inventory screen.','The controller explicitly replicates and remains only relevant to its owner; widget and open state remain non-replicated.','No item use, stack splitting/merging, world dropping, equipment, or crafting is introduced.'],
 'compiled_blueprints':compiled,'tests':tests,'pickup_regression':regression,
 'test_notes':['Client RPC behavior was verified with physical mouse input. Calling RPCs through editor Python executes within the editor script context and was not used as evidence of network routing.','Unreal Python did not return usable cached widget geometry; native mouse tests used the preview client rectangle and layout DPI scale.'],
 'manual_checks_remaining':['14-player stress test and latency/packet-loss tests.','Separate-process standalone/packaged game drag-and-drop and visual review on other display scales.'],
 'test_sessions_stopped':True
}
report['passed_drag_checks']=sum(len(t['checks']) for t in tests.values());report['passed_pickup_regression_checks']=len(regression['checks'])
(out/'drag-and-drop-report.json').write_text(json.dumps(report,indent=2))
print('DRAG_VALIDATED',report['passed_drag_checks'],'drag checks;',len(compiled),'clean Blueprints;',len(regression['checks']),'pickup/door regression checks')
