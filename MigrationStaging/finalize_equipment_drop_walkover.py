import unreal,json,toolset_registry
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
paths=['/Game/AIExample/Items/BP_ItemPickup','/Game/AIExample/UI/WBP_Inventory','/Game/AIExample/UI/BP_InventoryDragOperation','/Game/Blueprints/SandboxCharacter_CMC_ABP']
for path in paths:
 bp=unreal.load_asset(path)
 with toolset_registry.tool_raising_exceptions():B.compile_blueprint(bp,warnings_as_errors=True)
 assert bp.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE,path
 assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
settings=unreal.ValidateAssetsSettings(validation_usecase=unreal.DataValidationUsecase.COMMANDLET,collect_per_asset_details=True)
ret,res=unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem).validate_assets_with_settings([unreal.EditorAssetLibrary.find_asset_data(p) for p in paths],settings)
stats={k:res.get_editor_property(k) for k in ['num_checked','num_valid','num_invalid','num_warnings']}
assert stats['num_invalid']==0 and stats['num_warnings']==0,stats
out=Path(unreal.Paths.project_saved_dir())/'EquipmentValidation';tests={n:json.loads((out/(n+'-result.json')).read_text()) for n in ['walkover','equipment-drop-mouse']}
assert all(t['passed'] for t in tests.values())
report={'status':'fixed','changes':['Loose weapons ignore Pawn collision and cannot be stepped on. Gravity and scenery collision remain enabled.','GASP foot placement uses Camera trace channel, which loose weapons also ignore; Visibility remains blocking for pickup interaction.','Backpack drag payload captures stable weapon instance and layout version. Equipment drops use the existing authoritative transfer RPC.','Pistols/revolvers use Sidearm; long guns use Primary/Secondary. Compatible occupied equipment swaps with the dragged backpack weapon.','Invalid, stale and outside drops preserve weapons. Existing backpack rearrangement and right-click unequip remain available.'], 'validation':stats,'tests':tests,'manual_review':['Visual foot placement on additional stairs/slopes and custom scenery collision profiles.','Packaged and 14-player network tests were not run.']}
(out/'equipment-drop-walkover-report.json').write_text(json.dumps(report,indent=2));print('VALIDATED',stats)
