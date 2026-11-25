import unreal,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import asset,save
paths=['Items/BP_InventoryComponent','Items/BP_InventoryPlayerController','Interaction/BP_SurvivorInteractionCharacter','Interaction/BP_InteractionHUD','Combat/BP_PistolTarget','Combat/Animation/ABP_SurvivorCombat']
assets=[asset(p) for p in paths]
for bp in assets:save(bp)
for p in unreal.EditorAssetLibrary.list_assets('/Game/AIExample/Combat',recursive=True,include_folder=False):
 a=unreal.load_asset(p)
 if a and a not in assets:assets.append(a)
assets.extend([asset('Interaction/IMC_SurvivorInteraction'),asset('Items/DA_PistolItem'),asset('Weapons/TheHouse/04_Weapons/Pistol/Mesh/SM_Pistol')])
for a in assets:assert unreal.EditorAssetLibrary.save_loaded_asset(a,only_if_is_dirty=False)
settings=unreal.ValidateAssetsSettings(validation_usecase=unreal.DataValidationUsecase.COMMANDLET,collect_per_asset_details=True)
ret,res=unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem).validate_assets_with_settings([unreal.EditorAssetLibrary.find_asset_data(a.get_path_name()) for a in assets],settings)
report={k:res.get_editor_property(k) for k in ['num_checked','num_valid','num_invalid','num_warnings']}
report['blueprints_compiled']=paths;report['passed']=report['num_invalid']==0
(Path(unreal.Paths.project_saved_dir())/'PistolCombatValidation/asset-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report));assert report['passed']
