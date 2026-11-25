import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
R='/Game/AIExample/';checks={}
inv=unreal.load_asset(R+'Items/BP_InventoryComponent');pc=unreal.load_asset(R+'Items/BP_InventoryPlayerController');ui=unreal.load_asset(R+'UI/WBP_Inventory')
checks['pickup_registers_weapon']='RegisterWeapon' in B.read_graph_dsl(B.get_graph(inv,'TryAddItem'))
checks['transaction_saved']=len(B.read_graph_dsl(B.get_graph(inv,'TryTransferWeapon')))>5000
checks['request_calls_RPC']='ServerTransferWeapon' in B.read_graph_dsl(B.get_graph(pc,'RequestEquipmentTransfer'))
checks['equipment_refresh_saved']='RefreshEquipment' in B.read_graph_dsl(B.get_graph(ui,'RefreshInventory'))
checks['input_keys_saved']={str(m.get_editor_property('key').export_text()) for m in unreal.load_asset(R+'Interaction/IMC_SurvivorInteraction').get_editor_property('default_key_mappings').get_editor_property('mappings')}=={'E','I'}
checks['defaults_empty']=list(unreal.get_default_object(inv.generated_class()).get_editor_property('EquipmentInstances'))==['','','']
report={'checks':checks,'passed':all(checks.values()),'method':'separate headless Unreal process reading saved packages'}
(Path(unreal.Paths.project_saved_dir())/'EquipmentValidation/disk-reload-result.json').write_text(json.dumps(report,indent=2))
assert report['passed'],report
print('EQUIPMENT_DISK_RELOAD_PASS')
