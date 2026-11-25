import unreal,json,hashlib
from pathlib import Path
p=Path(unreal.Paths.project_dir()).resolve();assert p.name=='AIExample'
w=p/'MigrationStaging/Pistol-20261117-101027'
report=w/'staging-validation.json'
if not report.is_file():report=p.parent/'AIExample-Archive/DirectoryCleanup-20261124/Migrations/Pistol-20261117-101027/staging-validation.json'
staged=json.loads(report.read_text())
w.mkdir(parents=True,exist_ok=True)
expected=set(staged['packages'])
r=unreal.AssetRegistryHelpers.get_asset_registry();r.search_all_assets(True);r.scan_paths_synchronous(['/Game/AIExample/Weapons/TheHouse'],True)
assets=r.get_assets_by_path('/Game/AIExample/Weapons/TheHouse',recursive=True)
assert {str(a.package_name) for a in assets}==expected
opts=unreal.AssetRegistryDependencyOptions(include_hard_package_references=True,include_soft_package_references=True)
classes={};edges={};loaded=[]
for a in sorted(expected):
 o=unreal.load_asset(a);assert o and not isinstance(o,unreal.Blueprint),a
 loaded.append(o);classes[a]=o.get_class().get_name()
 assert classes[a]!='ObjectRedirector'
 edges[a]=sorted(str(d) for d in r.get_dependencies(a,opts))
 assert edges[a]==sorted(staged['edges'][a]),(a,edges[a],staged['edges'][a])
 for d in edges[a]:
  if not d.startswith('/Script/'):assert unreal.EditorAssetLibrary.does_asset_exist(d),(a,d)
settings=unreal.ValidateAssetsSettings(validation_usecase=unreal.DataValidationUsecase.COMMANDLET,collect_per_asset_details=True)
ret,res=unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem).validate_assets_with_settings(assets,settings)
stats={k:res.get_editor_property(k) for k in ['num_requested','num_checked','num_valid','num_invalid','num_skipped','num_warnings','num_unable_to_validate']}
report={'validation':stats,'dependency_graph_matches_staging':True,'classes':classes,'details':str(res.get_editor_property('assets_details'))}
(w/'destination-validation.json').write_text(json.dumps(report,indent=2))
assert stats['num_invalid']==0,stats
unreal.log('PISTOL_DESTINATION_VALIDATED '+str(stats))
