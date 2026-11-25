import unreal,json,shutil,datetime
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
root=Path(unreal.Paths.project_dir()).resolve();out=Path(unreal.Paths.project_saved_dir())/'LocomotionRepair'
backup=root/'Backups'/('BeforeLocomotionRepair-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir(parents=True)
paths=json.loads((Path(unreal.Paths.project_saved_dir())/'ShoulderCamera/repaired-animation-contexts.json').read_text())
paths+=['/Game/Blueprints/SandboxCharacter_CMC_ABP','/Game/AIExample/Combat/Animation/ABP_SurvivorCombat','/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter']
for path in paths:shutil.copy2(root/'Content'/(path[6:]+'.uasset'),backup/(path.rsplit('/',1)[1]+'.uasset'))
(out/'backup.json').write_text(json.dumps({'path':str(backup),'assets':paths},indent=2))
for path in paths[:5]:
 c=unreal.load_asset(path);contexts=c.get_editor_property('context_data')
 for i in range(len(contexts)):
  v=contexts[i];v.import_text(v.export_text().replace('/Game/AIExample/Combat/Animation/ABP_SurvivorCombat.ABP_SurvivorCombat_C','/Game/Blueprints/SandboxCharacter_CMC_ABP.SandboxCharacter_CMC_ABP_C'));contexts[i]=v
 c.set_editor_property('context_data',contexts);unreal.EditorAssetLibrary.save_loaded_asset(c,only_if_is_dirty=False)
for path in paths[5:7]:
 bp=unreal.load_asset(path)
 print('COMPILE',path)
 B.compile_blueprint(bp,warnings_as_errors=True)
 print('STATUS',bp.get_editor_property('status'))
