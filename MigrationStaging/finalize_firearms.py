import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();saved=root/'Saved';R='/Game/AIExample/'
files=['extra-firearms-result.json','shotgun-spread-cover-result.json','nearby-revolver-result.json','nearby-shotgun-result.json','firearm-niagara-result.json','firearm-multiplayer-result.json','firearm-aim-result.json']
report={name:json.loads((saved/name).read_text()) for name in files}
assert all(r['passed'] for r in report.values())
char=unreal.load_asset(R+'Interaction/BP_SurvivorInteractionCharacter');cdo=unreal.get_default_object(char.generated_class())
assert abs(cdo.get_editor_property('CameraWalkDistance')-250.0)<.01
report['camera_walk_distance_cm']=250
report['attachment_mesh']='/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin'
report['placement']='Named sockets; SnapToTarget; no weapon component translation or rotation offsets.'
report['tuning']={'revolver_capacity':6,'revolver_damage':55,'shotgun_capacity':2,'shotgun_pellets':8,'shotgun_pellet_damage':18,'shotgun_spread_radius_at_10m_cm':65,'shotgun_max_range_m':30,'normal_run_after_shot_s':2.5}
(saved/'FirearmValidation.json').write_text(json.dumps(report,indent=2))
for rel in ['Items/BP_InventoryComponent','Interaction/BP_SurvivorInteractionCharacter','Items/BP_InventoryPlayerController','Interaction/BP_InteractionHUD','UI/WBP_Inventory','Combat/NS_RevolverMuzzle','Combat/NS_ShotgunMuzzle','Combat/NS_BulletImpact','Combat/BP_BulletTracer','Combat/M_BulletTracer','Combat/Animation/Revolver_Reload']:
 assert unreal.EditorAssetLibrary.save_loaded_asset(unreal.load_asset(R+rel),only_if_is_dirty=True)
mesh=unreal.load_asset(report['attachment_mesh']);assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=True)
ed=unreal.get_editor_subsystem(unreal.AssetEditorSubsystem);ed.open_editor_for_assets([mesh])
print('FIREARMS_FINAL_VALIDATION_PASSED',len(files),'reports')
