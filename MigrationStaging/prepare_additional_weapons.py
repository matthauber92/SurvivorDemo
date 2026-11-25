from pathlib import Path
import json,hashlib,shutil,re
project=Path(__file__).resolve().parent.parent
source=project.parent/'TheHouse/TheHouse 5.8';work=project/'MigrationStaging/AdditionalWeapons'
roots=['/Game/'+p for p in [
 '04_Weapons/Revolver/Mesh/SM_Revolver','04_Weapons/Revolver/Mesh/SKM_Revolver','04_Weapons/Revolver/Image/IMG_Revolver',
 '04_Weapons/Shotgun/Mesh/SKM_Shotgun','04_Weapons/Shotgun/Image/IMG_Shotgun',
 '05_InventoryAssets/Bullets/PistolBullets/Mesh/SM_Pistol_Ammo','05_InventoryAssets/Bullets/PistolBullets/Image/IMG_Pistol_Ammo',
 '05_InventoryAssets/Bullets/RevolverBullets/Mesh/SM_Revolver_Ammo','05_InventoryAssets/Bullets/RevolverBullets/Image/IMG_Revolver_Bullets',
 '05_InventoryAssets/Bullets/ShotgunBullets/Mesh/Shotgun_Bullets','05_InventoryAssets/Bullets/ShotgunBullets/Image/IMG_Shotgun_Bullets',
 '06_SFX/GunSFX/Revolver/SFX_Revolver_Shot_2','06_SFX/GunSFX/Revolver/Revolver_Load_Bullet_Cue','06_SFX/GunSFX/Revolver/Revolver_Close_Cue',
 '06_SFX/GunSFX/Shotgun/Shotgun_Shoot_Cue','06_SFX/GunSFX/Shotgun/Shotgun_Reload_Slow_Cue','06_SFX/GunSFX/Shotgun/Shotgun_Reload_Closing_Barrel_Cue',
 '07_ParticleFX/Pistol/NS_Pistol','07_ParticleFX/Pistol/Sources/Meshes/SM_Bullet_Casing_Shotgun','07_ParticleFX/Pistol/Sources/Meshes/SM_bullet_casing_9mm']]
seen=set();pending=list(roots);hashes={}
while pending:
 a=pending.pop()
 if a in seen:continue
 seen.add(a);p=source/'Content'/(a[6:]+'.uasset');assert p.exists(),p
 hashes[a]=hashlib.sha256(p.read_bytes()).hexdigest()
 for raw in re.findall(rb'[ -~]{5,}',p.read_bytes()):
  value=raw.decode('ascii')
  if re.fullmatch(r'/Game/[A-Za-z0-9_/\-]+',value) and (source/'Content'/(value[6:]+'.uasset')).exists():pending.append(value)
for name in ['SourceCopy','Stage']:
 d=work/name;(d/'Content').mkdir(parents=True,exist_ok=True)
 (d/(name+'.uproject')).write_text(json.dumps({'FileVersion':3,'EngineAssociation':'5.8','Plugins':[{'Name':n,'Enabled':True} for n in ['PythonScriptPlugin','EditorScriptingUtilities','Niagara']]},indent=2))
for a in seen:
 rel=Path(a[6:]+'.uasset');dest=work/'SourceCopy/Content'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/'Content'/rel,dest)
(work/'manifest.json').write_text(json.dumps({'project':str(project),'source':str(source),'work':str(work),'roots':roots,'source_hashes':hashes},indent=2))
print('PREPARED',len(seen),work)
