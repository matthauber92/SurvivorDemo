import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
R='/Game/AIExample/'
def graph(p,n):return B.read_graph_dsl(B.get_graph(unreal.load_asset(R+p),n))
checks={}
checks['reload_transaction_saved']='ReloadTransferAmount' in graph('Items/BP_InventoryComponent','TickPistolCombat')
checks['server_action_saved']='TryPistolAction' in graph('Items/BP_InventoryPlayerController','EventGraph')
checks['muzzle_effect_scaled']='0.18' in graph('Interaction/BP_SurvivorInteractionCharacter','PlayPistolShot')
checks['aim_state_saved']='CharacterInputState' in graph('Interaction/BP_SurvivorInteractionCharacter','RefreshPistolAim')
checks['ammo_HUD_saved']='DrawText' in graph('Interaction/BP_InteractionHUD','DrawPistolHUD')
checks['muzzle_socket_saved']=unreal.load_asset(R+'Weapons/TheHouse/04_Weapons/Pistol/Mesh/SM_Pistol').find_socket('Muzzle') is not None
keys={str(m.get_editor_property('key').export_text()) for m in unreal.load_asset(R+'Interaction/IMC_SurvivorInteraction').get_editor_property('default_key_mappings').get_editor_property('mappings')}
checks['combat_keys_saved']={'RightMouseButton','LeftMouseButton','R'}.issubset(keys)
anim=unreal.load_asset(R+'Combat/Animation/Survivor_MM_Pistol_Reload')
checks['reload_sound_notifies_saved']=len(unreal.AnimationLibrary.get_animation_notify_events(anim))>=3
checks['combat_anim_class_saved']=unreal.load_class(None,R+'Combat/Animation/ABP_SurvivorCombat.ABP_SurvivorCombat_C') is not None
report={'checks':checks,'passed':all(checks.values()),'method':'fresh headless Unreal process reading saved packages'}
(Path(unreal.Paths.project_saved_dir())/'PistolCombatValidation/disk-reload-result.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report));assert report['passed'],report
