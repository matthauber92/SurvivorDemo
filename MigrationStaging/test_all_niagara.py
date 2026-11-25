import unreal,json,time,traceback
from pathlib import Path
fx_world=unreal.EditorLevelLibrary.get_pie_worlds(False)[0]
fx_results={};fx_components=[]
for fx_path in ['/Game/AIExample/Weapons/TheHouse/07_ParticleFX/Pistol/NS_Pistol','/Game/AIExample/Combat/NS_RevolverMuzzle','/Game/AIExample/Combat/NS_ShotgunMuzzle','/Game/AIExample/Combat/NS_BulletImpact']:
 fx_component=unreal.NiagaraFunctionLibrary.spawn_system_at_location(fx_world,unreal.load_asset(fx_path),unreal.Vector(0,0,300),auto_destroy=False,auto_activate=True,pre_cull_check=False)
 fx_results[fx_path]=bool(fx_component and fx_component.is_active());fx_components.append(fx_component)
(Path(unreal.Paths.project_saved_dir())/'firearm-niagara-result.json').write_text(json.dumps({'systems':fx_results,'passed':all(fx_results.values())},indent=2))
assert all(fx_results.values()),fx_results
print('ALL_FIREARM_NIAGARA_ACTIVE',fx_results)
