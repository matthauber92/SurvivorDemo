import unreal,shutil,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();changed=[]
old='/Game/Blueprints/SandboxCharacter_CMC_ABP.SandboxCharacter_CMC_ABP_C';new='/Game/AIExample/Combat/Animation/ABP_SurvivorCombat.ABP_SurvivorCombat_C'
for a in unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_class(unreal.TopLevelAssetPath('/Script/Chooser','ChooserTable'),True):
 path=str(a.package_name)
 if path.startswith('/Game/AIExample/Combat/Animation/CHT_'):continue
 c=a.get_asset();contexts=c.get_editor_property('context_data')
 if not any(old in ctx.export_text() for ctx in contexts):continue
 src=root/'Content'/(path[6:]+'.uasset');dst=root/'Backups/BeforeShoulderCamera-20261117-124627'/src.name;dst.parent.mkdir(parents=True,exist_ok=True)
 if not dst.exists():shutil.copy2(src,dst)
 for j in range(len(contexts)):
  ctx=contexts[j];ctx.import_text(ctx.export_text().replace(old,new));contexts[j]=ctx
 c.set_editor_property('context_data',contexts);assert unreal.EditorAssetLibrary.save_loaded_asset(c,only_if_is_dirty=False);changed.append(path)
(Path(unreal.Paths.project_saved_dir())/'ShoulderCamera/repaired-animation-contexts.json').write_text(json.dumps(changed,indent=2));print(changed)
# Remove only the four unused inspection copies created by fix_combat_choosers.py.
for suffix in ['', '_Dense','_Sparse','_ExtremeSparse']:
 path='/Game/AIExample/Combat/Animation/CHT_PoseSearchDatabases'+suffix
 if unreal.EditorAssetLibrary.does_asset_exist(path):unreal.EditorAssetLibrary.delete_asset(path)
