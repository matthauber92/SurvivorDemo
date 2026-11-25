import unreal,json,hashlib
from pathlib import Path
p=Path(unreal.Paths.project_dir()).resolve()
assert p.name=='Stage'
w=p.parent;m=json.loads((w/'manifest.json').read_text())
project=Path(m['project']);mapping=json.loads((w/'path-mapping.json').read_text())
reg=unreal.AssetRegistryHelpers.get_asset_registry();reg.search_all_assets(True);reg.scan_paths_synchronous(['/Game'],True)
assets=reg.get_assets_by_path('/Game',recursive=True)
redirectors=[str(a.package_name) for a in assets if str(a.asset_class_path.asset_name)=='ObjectRedirector']
assert not redirectors,redirectors
expected=set(mapping.values()); actual={str(a.package_name) for a in assets}
assert actual==expected,{'unexpected':list(actual-expected),'missing':list(expected-actual)}
opts=unreal.AssetRegistryDependencyOptions(include_hard_package_references=True,include_soft_package_references=True)
edges={};external=set();loaded=[]
for a in sorted(expected):
 obj=unreal.load_asset(a); assert obj and not isinstance(obj,unreal.Blueprint),a
 loaded.append(obj)
 deps=[str(d) for d in reg.get_dependencies(a,opts)];edges[a]=deps
 for d in deps:
  if d.startswith('/Game/'): assert d in expected,(a,d)
  elif not d.startswith('/Script/'):
   assert unreal.EditorAssetLibrary.does_asset_exist(d),('missing external',d)
   external.add(d)
settings=unreal.ValidateAssetsSettings()
settings.set_editor_property('collect_per_asset_details',True)
settings.set_editor_property('validation_usecase',unreal.DataValidationUsecase.COMMANDLET)
sub=unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem)
ret,results=sub.validate_assets_with_settings(assets,settings)
stats={k:results.get_editor_property(k) for k in ['num_requested','num_checked','num_valid','num_invalid','num_skipped','num_warnings','num_unable_to_validate']}
report={'packages':sorted(expected),'edges':edges,'external':sorted(external),'redirectors':redirectors,'validation':stats,'validation_details':str(results.get_editor_property('assets_details'))}
(w/'staging-validation.json').write_text(json.dumps(report,indent=2))
assert stats['num_invalid']==0,stats
def sha(f):
 h=hashlib.sha256()
 with f.open('rb') as stream:
  for block in iter(lambda:stream.read(1048576),b''):h.update(block)
 return h.hexdigest()
before=json.loads((w/'before.json').read_text())
changed=[r for r,h in before.items() if not (project/r).exists() or sha(project/r)!=h]
assert not changed,('Project changed since backup',changed)
conflicts=[a for a in expected if (project/'Content'/(a[6:]+'.uasset')).exists()]
assert not conflicts,conflicts
options=unreal.MigrationOptions(prompt=False,ignore_dependencies=False,asset_conflict=unreal.AssetMigrationConflict.SKIP)
unreal.AssetToolsHelpers.get_asset_tools().migrate_packages([mapping[a] for a in m['roots']],str(project/'Content'),options)
missing=[a for a in expected if not (project/'Content'/(a[6:]+'.uasset')).exists()]
changed=[r for r,h in before.items() if not (project/r).exists() or sha(project/r)!=h]
source_changed=[a for a,h in m['source_hashes'].items() if sha(Path(m['source'])/'Content'/(a[6:]+'.uasset'))!=h]
delivered={a:sha(project/'Content'/(a[6:]+'.uasset')) for a in expected if a not in missing}
mismatched=[a for a,h in delivered.items() if sha(p/'Content'/(a[6:]+'.uasset'))!=h]
result={'api':'unreal.AssetTools.migrate_packages','roots':[mapping[a] for a in m['roots']],'package_count':len(expected),'missing':missing,'existing_files_changed':changed,'source_files_changed':source_changed,'staging_destination_hash_mismatches':mismatched,'backup':m['backup'],'validation':stats,'delivered_hashes':delivered}
(w/'migration-result.json').write_text(json.dumps(result,indent=2))
assert not (missing or changed or source_changed or mismatched),result
unreal.log('PISTOL_MIGRATION_VERIFIED '+str(stats))
