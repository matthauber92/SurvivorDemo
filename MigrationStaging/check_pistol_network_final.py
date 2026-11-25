import unreal,json
from pathlib import Path
ws=unreal.EditorLevelLibrary.get_pie_worlds(False)
sw=next(w for w in ws if unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
cw=next(w for w in ws if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
cp=unreal.GameplayStatics.get_player_pawn(cw,0)
sp=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(sw,cp.get_class()) if not p.is_locally_controlled())
ci=cp.get_controller().get_editor_property('InventoryComponent');si=sp.get_controller().get_editor_property('InventoryComponent')
checks={}
checks['magazine_matches_server']=list(ci.get_editor_property('WeaponMagazines'))==list(si.get_editor_property('WeaponMagazines'))==[15]
checks['reserve_matches_server']=ci.call_method('GetItemQuantity',(unreal.Name('Ammo.Handgun'),))==si.call_method('GetItemQuantity',(unreal.Name('Ammo.Handgun'),))==13
checks['shot_serial_replicated']=cp.get_editor_property('PublicShotSerial')==sp.get_editor_property('PublicShotSerial')==2
uid=si.get_editor_property('ActiveWeaponInstance');origin=sp.get_actor_location()+unreal.Vector(0,0,60);direction=sp.get_control_rotation().get_forward_vector()
checks['client_cannot_apply_direct_action']=not ci.call_method('TryPistolAction',(2,uid,origin,direction))
checks['stale_instance_rejected']=not si.call_method('TryPistolAction',(2,'stale-instance',origin,direction))
checks['spoofed_origin_rejected']=not si.call_method('TryPistolAction',(2,uid,origin+unreal.Vector(5000,0,0),direction))
checks['backward_direction_rejected']=not si.call_method('TryPistolAction',(2,uid,origin,direction*-1))
checks['full_magazine_reload_rejected']=not si.call_method('TryPistolAction',(3,uid,origin,direction))
checks['rejected_actions_preserve_ammo']=list(si.get_editor_property('WeaponMagazines'))==[15]
checks['combat_anim_on_both_pawns']=all(p.get_component_by_class(unreal.SkeletalMeshComponent).get_anim_instance().get_class().get_name()=='ABP_SurvivorCombat_C' for p in [cp,sp])
report={'checks':checks,'passed':all(checks.values())}
(Path(unreal.Paths.project_saved_dir())/'PistolCombatValidation/network-final.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
