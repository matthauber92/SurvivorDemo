import unreal, json, hashlib
from pathlib import Path

p = Path(unreal.Paths.project_dir()).resolve()
w = p.parent
m = json.loads((w/'manifest.json').read_text())
assert str(w)==m['work'] and p.name in ['SourceCopy','Stage']
reg = unreal.AssetRegistryHelpers.get_asset_registry()
reg.search_all_assets(True)
reg.scan_paths_synchronous(['/Game'],True)
at = unreal.AssetToolsHelpers.get_asset_tools()
def closure(roots):
 seen=set(); todo=list(roots); external=set(); edges={}
 opts=unreal.AssetRegistryDependencyOptions()
 opts.set_editor_property('include_hard_package_references',True)
 opts.set_editor_property('include_soft_package_references',True)
 while todo:
  a=todo.pop()
  if a in seen: continue
  seen.add(a)
  assert unreal.EditorAssetLibrary.does_asset_exist(a), 'Missing '+a
  deps=[str(x) for x in reg.get_dependencies(a,opts)]
  edges[a]=deps
  for d in deps:
   if d.startswith('/Game/'): todo.append(d)
   else: external.add(d)
 return {'packages':sorted(seen),'external':sorted(external),'edges':edges}
def migrate(roots,target):
 opts=unreal.MigrationOptions()
 opts.set_editor_property('prompt',False)
 opts.set_editor_property('ignore_dependencies',False)
 opts.set_editor_property('asset_conflict',unreal.AssetMigrationConflict.SKIP)
 at.migrate_packages(roots,str(target),opts)

if p.name=='SourceCopy':
 report=closure(m['roots'])
 assert set(report['packages']) <= set(m['source_hashes']), report
 for a in report['packages']:
  obj=unreal.load_asset(a)
  assert obj and not isinstance(obj,unreal.Blueprint),a
 (w/'source-dependencies.json').write_text(json.dumps(report,indent=2))
 migrate(m['roots'],w/'Stage'/'Content')
 missing=[a for a in report['packages'] if not (w/'Stage'/'Content'/(a[6:]+'.uasset')).exists()]
 assert not missing, missing
 (w/'source-migration-result.json').write_text(json.dumps({'packages':len(report['packages']),'missing':missing,'api':'AssetTools.migrate_packages'},indent=2))
else:
 report=json.loads((w/'source-dependencies.json').read_text())
 mapping={a:'/Game/AIExample/Weapons/TheHouse/'+a[6:] for a in report['packages']}
 renames=[]
 for old,new in mapping.items():
  assert not unreal.EditorAssetLibrary.does_asset_exist(new),new
  obj=unreal.load_asset(old)
  assert obj and not isinstance(obj,unreal.Blueprint),old
  folder,name=new.rsplit('/',1)
  renames.append(unreal.AssetRenameData(obj,folder,name))
 assert at.rename_assets(renames),'Rename failed'
 assert unreal.EditorAssetLibrary.save_directory('/Game',only_if_is_dirty=False,recursive=True)
 (w/'path-mapping.json').write_text(json.dumps(mapping,indent=2))
 (w/'stage-api.json').write_text(json.dumps({'validation':unreal.EditorValidatorSubsystem.validate_assets_with_settings.__doc__},indent=2))
unreal.log('PISTOL_SCRIPT_SUCCESS')
