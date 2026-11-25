import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A
R='/Game/AIExample/';checks={}
inv=unreal.load_asset(R+'Items/BP_InventoryComponent');pc=unreal.load_asset(R+'Items/BP_InventoryPlayerController');char=unreal.load_asset(R+'Interaction/BP_SurvivorInteractionCharacter')
checks['authoritative_selection_saved']='HasAuthority' in B.read_graph_dsl(B.get_graph(inv,'TrySelectWeapon'))
checks['request_calls_server_RPC']='ServerSelectWeapon' in B.read_graph_dsl(B.get_graph(pc,'RequestSelectWeapon'))
checks['inventory_reconciles_active_weapon']='SyncWeaponPresentation' in B.read_graph_dsl(B.get_graph(inv,'NotifyInventoryChanged'))
checks['public_repnotifies_refresh_visuals']=all('RefreshWeaponVisuals' in B.read_graph_dsl(B.get_graph(char,'OnRep_'+n)) for n in ['PublicPrimary','PublicSecondary','PublicSidearm','PublicActiveSlot'])
checks['starts_holstered']=unreal.get_default_object(char.generated_class()).get_editor_property('PublicActiveSlot')==-1 and unreal.get_default_object(inv.generated_class()).get_editor_property('ActiveWeaponInstance')==''
checks['all_five_input_keys_saved']={m.get_editor_property('key').export_text() for m in unreal.load_asset(R+'Interaction/IMC_SurvivorInteraction').get_editor_property('default_key_mappings').get_editor_property('mappings')}=={'E','I','One','Two','Three'}
events=[B._get_node_info(n) for n in B.find_nodes(B.get_graph(pc,'EventGraph')) if isinstance(n,unreal.K2Node_EnhancedInputAction)]
checks['three_started_bindings_saved']=sum(1 for e in events if 'IA_Select' in e.type_id and any(p.name=='Started' and p.connected_pins for p in e.output_pins))==3
components=[c for c in A.get_components(unreal.get_default_object(char.generated_class())) if any(n in c.get_name() for n in ['PrimaryVisual','SecondaryVisual','SidearmVisual'])]
checks['cosmetics_have_no_collision']=len(components)==3 and all(c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION for c in components)
checks['back_offsets_saved']='10,-18' in B.read_graph_dsl(B.get_graph(char,'UpdateWeaponVisual')).replace(' ','')
report={'checks':checks,'passed':all(checks.values()),'method':'separate headless Unreal process reading saved packages'}
(Path(unreal.Paths.project_saved_dir())/'WeaponSwitchValidation/disk-result.json').write_text(json.dumps(report,indent=2))
assert report['passed'],report
print('WEAPON_DISK_RELOAD_PASS')
