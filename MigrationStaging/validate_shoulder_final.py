import unreal,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
paths=['Interaction/BP_SurvivorInteractionCharacter','Interaction/BP_InteractionHUD','Items/BP_InventoryPlayerController','Items/BP_InventoryComponent','Combat/Animation/ABP_SurvivorCombat']
assets=[asset(p) for p in paths]
for bp in assets:save(bp)
mesh=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin');assets.append(mesh)
out=Path(unreal.Paths.project_saved_dir())/'ShoulderCamera'
for path in json.loads((out/'repaired-animation-contexts.json').read_text()):assets.append(unreal.load_asset(path))
for a in assets:assert unreal.EditorAssetLibrary.save_loaded_asset(a,only_if_is_dirty=False)
settings=unreal.ValidateAssetsSettings(validation_usecase=unreal.DataValidationUsecase.COMMANDLET,collect_per_asset_details=True)
ret,res=unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem).validate_assets_with_settings([unreal.EditorAssetLibrary.find_asset_data(a.get_path_name()) for a in assets],settings)
report={k:res.get_editor_property(k) for k in ['num_checked','num_valid','num_invalid','num_warnings']}
report['camera_distances_cm']={'walking':350,'sprinting':600,'aiming':220,'hip_firing':300}
report['crosshair']='Aiming or one second after a shot; hidden during reload and inventory.'
report['grip_socket_rotation']=str(mesh.find_socket('PistolGrip_R').get_editor_property('relative_rotation'))
report['controls']=json.loads((out/'controls-result.json').read_text())['passed']
report['client_controls']=json.loads((out/'client-controls-result.json').read_text())['passed']
report['passed']=report['num_invalid']==0 and report['controls'] and report['client_controls']
(out/'final-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));assert report['passed']
