import unreal,json,toolset_registry
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
R='/Game/AIExample/';paths=[R+'Items/BP_ItemPickup',R+'Weapons/TheHouse/04_Weapons/Pistol/Mesh/SM_Pistol',R+'Maps/Lvl_EquipmentTest']
bp=unreal.load_asset(paths[0])
with toolset_registry.tool_raising_exceptions():B.compile_blueprint(bp,warnings_as_errors=True)
assert bp.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE
assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
settings=unreal.ValidateAssetsSettings(validation_usecase=unreal.DataValidationUsecase.COMMANDLET,collect_per_asset_details=True)
ret,res=unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem).validate_assets_with_settings([unreal.EditorAssetLibrary.find_asset_data(p) for p in paths],settings)
stats={k:res.get_editor_property(k) for k in ['num_checked','num_valid','num_invalid','num_warnings']}
assert stats['num_invalid']==0 and stats['num_warnings']==0,stats
out=Path(unreal.Paths.project_saved_dir())/'EquipmentValidation'
tests={n:json.loads((out/(n+'.json')).read_text()) for n in ['ground-gun-result','ground-pickup-keyboard-result','ground-physics-multiplayer-result']}
assert all(t['passed'] for t in tests.values()),tests
report={'status':'fixed','changes':['Pistol convex collision for interaction traces and physics.','PickupMesh promoted to root so physics and actor transforms stay together.','Weapon gravity and replicated physical movement enabled.','Test guns placed at ground level; pistol uses full imported scale.'],'validation':stats,'tests':tests}
(out/'pickup-physics-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(stats))
