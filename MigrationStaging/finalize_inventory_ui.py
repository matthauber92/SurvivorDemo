import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out=Path(unreal.Paths.project_saved_dir())/'InventoryUIValidation'
compiled={}
for path in ['UI/WBP_Inventory','Items/BP_InventoryPlayerController','Items/BP_InventoryComponent','Items/BP_ItemPickup','Items/BP_PickupTestGameMode','Interaction/BP_SurvivorInteractionCharacter','Interaction/BP_InteractionTestDoor']:
 b=unreal.load_asset('/Game/AIExample/'+path);B.compile_blueprint(b,warnings_as_errors=True);status=str(b.get_editor_property('status'));assert status=='<BlueprintStatus.BS_UP_TO_DATE: 3>',(path,status);compiled[path]=status
 unreal.EditorAssetLibrary.save_loaded_asset(b)
 if path in ['UI/WBP_Inventory','Items/BP_InventoryPlayerController','Items/BP_InventoryComponent']:(out/(b.get_name()+'-final-graphs.json')).write_text(json.dumps({g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(b)},indent=2))
pc=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');inv=unreal.load_asset('/Game/AIExample/Items/BP_InventoryComponent')
print('UI_REPLICATION',{n:str(B.get_variable_replication(pc,n)) for n in ['InventoryWidget','InventoryOpen']})
print('INVENTORY_REPLICATION',{n:str(B.get_variable_replication(inv,n)) for n in ['ItemIDs','Quantities']})
assert 'NotifyInventoryChanged' in B.read_graph_dsl(B.get_graph(inv,'TryAddItem'))
c=unreal.load_asset('/Game/AIExample/Interaction/IMC_SurvivorInteraction');mappings=[m.export_text() for m in c.get_editor_property('default_key_mappings').get_editor_property('mappings')]
assert len(mappings)==2 and any('Key=I,' in m and 'IA_ToggleInventory' in m for m in mappings) and any('Key=E,' in m and 'IA_SurvivorInteract' in m for m in mappings)
(out/'blueprint-validation.json').write_text(json.dumps({'compiled':compiled,'input_mappings':mappings,'ui_replication':{n:str(B.get_variable_replication(pc,n)) for n in ['InventoryWidget','InventoryOpen']}},indent=2))
print('FINAL_COMPILE_PASS',len(compiled))
