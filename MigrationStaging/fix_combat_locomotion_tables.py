"""Give the copied combat AnimBP its own correctly typed chooser tables."""
import unreal,json,datetime,shutil
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
root=Path(unreal.Paths.project_dir());backup=root/'Backups'/('CombatLocomotionTables-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir(parents=True)
paths=json.loads((Path(unreal.Paths.project_saved_dir())/'ShoulderCamera/repaired-animation-contexts.json').read_text())
mapping={path:'/Game/AIExample/Combat/Animation/'+path.rsplit('/',1)[1] for path in paths}
for src,dst in mapping.items():
 disk=root/'Content'/(dst[6:]+'.uasset')
 if disk.exists():shutil.copy2(disk,backup/disk.name)
 if not unreal.EditorAssetLibrary.does_asset_exist(dst):assert unreal.EditorAssetLibrary.duplicate_asset(src,dst)
for src,dst in mapping.items():
 table=unreal.load_asset(dst)
 contexts=table.get_editor_property('context_data')
 for i,ctx in enumerate(contexts):
  ctx.import_text(ctx.export_text().replace('/Game/Blueprints/SandboxCharacter_CMC_ABP.SandboxCharacter_CMC_ABP_C','/Game/AIExample/Combat/Animation/ABP_SurvivorCombat.ABP_SurvivorCombat_C'));contexts[i]=ctx
 table.set_editor_property('context_data',contexts)
 results=table.get_editor_property('results_structs')
 for i,result in enumerate(results):
  txt=result.export_text()
  for a,b in mapping.items():txt=txt.replace(a+'.'+a.rsplit('/',1)[1],b+'.'+b.rsplit('/',1)[1])
  result.import_text(txt);results[i]=result
 table.set_editor_property('results_structs',results)
 assert unreal.EditorAssetLibrary.save_loaded_asset(table,only_if_is_dirty=False)
bp=unreal.load_asset('/Game/AIExample/Combat/Animation/ABP_SurvivorCombat')
shutil.copy2(root/'Content/AIExample/Combat/Animation/ABP_SurvivorCombat.uasset',backup/'ABP_SurvivorCombat.uasset')
for g in B.list_graphs(bp):
 for node in B.find_nodes(g):
  if 'EvaluateChooser:' not in B._get_node_info(node).type_id:continue
  old=node.get_editor_property('chooser')
  if old and old.get_path_name().split('.')[0] in mapping:
   node.set_editor_property('chooser',unreal.load_asset(mapping[old.get_path_name().split('.')[0]]));print('CHOOSER_FIXED',g.get_name())
B.compile_blueprint(bp,warnings_as_errors=True)
assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
