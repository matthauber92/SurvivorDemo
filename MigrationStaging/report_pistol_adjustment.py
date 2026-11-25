import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out=Path(unreal.Paths.project_saved_dir())/'PistolAdjustmentValidation'
paths=['/Game/AIExample/Items/BP_ItemPickup','/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter']
for path in paths:
 bp=unreal.load_asset(path)
 assert bp.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE
 assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
settings=unreal.ValidateAssetsSettings(validation_usecase=unreal.DataValidationUsecase.COMMANDLET,collect_per_asset_details=True)
_,res=unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem).validate_assets_with_settings([unreal.EditorAssetLibrary.find_asset_data(p) for p in paths],settings)
stats={n:res.get_editor_property(n) for n in ['num_checked','num_valid','num_invalid','num_warnings']}
tests={n:json.loads((out/(n+'-result.json')).read_text()) for n in ['targeting','walkover','multiplayer']}
assert all(t['passed'] for t in tests.values()) and stats['num_invalid']==stats['num_warnings']==0
report={'passed':True,'changes':['Pistol grip moved from wrist to palm; hand offset (-13,2,3).','Pistol lies flat at right hip, muzzle down and grip rearward; hip rotation pitch 0, yaw 180, roll -90.','Weapons have a 32 cm radius query-only interaction target attached to the physics mesh. Pawn, camera, foot IK, navigation and physics ignore this target.','Existing authoritative distance and line-of-sight validation retained.'],'visual_review':'In-game debug-camera closeups reviewed for both hand and hip.','validation':stats,'tests':tests}
(out/'report.json').write_text(json.dumps(report,indent=2))
(out/'graphs.json').write_text(json.dumps({'pickup':B.read_graph_dsl(B.get_graph(unreal.load_asset(paths[0]),'ApplyDefinitionMesh')),'visual':B.read_graph_dsl(B.get_graph(unreal.load_asset(paths[1]),'UpdateWeaponVisual'))},indent=2))
print('PISTOL_ADJUSTMENT_PASS',sum(len(t['checks']) for t in tests.values()),stats)
