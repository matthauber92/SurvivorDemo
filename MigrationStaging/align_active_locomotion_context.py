import unreal,json,datetime,shutil
from pathlib import Path
root=Path(unreal.Paths.project_dir());backup=root/'Backups'/('ActiveLocomotionContext-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir(parents=True)
paths=json.loads((Path(unreal.Paths.project_saved_dir())/'ShoulderCamera/repaired-animation-contexts.json').read_text())
for path in paths:
 src=root/'Content'/(path[6:]+'.uasset');shutil.copy2(src,backup/src.name)
 table=unreal.load_asset(path);contexts=table.get_editor_property('context_data')
 for i,ctx in enumerate(contexts):
  ctx.import_text(ctx.export_text().replace('/Game/Blueprints/SandboxCharacter_CMC_ABP.SandboxCharacter_CMC_ABP_C','/Game/AIExample/Combat/Animation/ABP_SurvivorCombat.ABP_SurvivorCombat_C'));contexts[i]=ctx
 table.set_editor_property('context_data',contexts)
 assert unreal.EditorAssetLibrary.save_loaded_asset(table,only_if_is_dirty=False)
 print('ALIGNED',path)
