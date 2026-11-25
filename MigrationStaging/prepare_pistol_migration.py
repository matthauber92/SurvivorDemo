from pathlib import Path
import json, hashlib, shutil, re, datetime

project = Path(__file__).resolve().parent.parent
source = Path(r'C:\Users\Matt Hauber\Documents\Unreal Projects\TheHouse\TheHouse 5.8')
stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
work = project / 'MigrationStaging' / ('Pistol-' + stamp)
backup = project / 'Backups' / ('BeforeMilestone5-' + stamp)
roots = ['/Game/' + p for p in [
 '04_Weapons/Pistol/Mesh/SKM_Pistol', '04_Weapons/Pistol/Mesh/SM_Pistol',
 '04_Weapons/Pistol/Image/IMG_Pistol', '06_SFX/GunSFX/Pistol/SC_Pistol_Fire',
 '06_SFX/GunSFX/Pistol/SC_Empty_Pistol', '06_SFX/GunSFX/Pistol/SC_Equip_Gun',
 '06_SFX/GunSFX/Pistol/Reload/Pistol_Add_Magazine_Cue',
 '06_SFX/GunSFX/Pistol/Reload/Pistol_Remove_Magazine_Cue',
 '06_SFX/GunSFX/Pistol/Reload/Pistol_Cocking_Slide_Cue', '07_ParticleFX/Pistol/NS_Pistol']]
def sha(p):
 h = hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576), b''): h.update(b)
 return h.hexdigest()
work.mkdir(parents=True); backup.mkdir()
before = {}
for name in ['AIExample.uproject','Content','Config','Plugins','Source']:
 p = project/name
 if not p.exists(): continue
 files = list(p.rglob('*')) if p.is_dir() else [p]
 for f in files:
  if not f.is_file(): continue
  rel = f.relative_to(project); dest = backup/rel
  dest.parent.mkdir(parents=True, exist_ok=True)
  digest = sha(f); shutil.copy2(f,dest)
  assert sha(dest)==digest and sha(f)==digest, str(f)
  before[rel.as_posix()] = digest
(work/'before.json').write_text(json.dumps(before,indent=2))
seen=set(); pending=list(roots); hashes={}
while pending:
 a=pending.pop()
 if a in seen: continue
 seen.add(a); p=source/'Content'/(a[6:]+'.uasset')
 assert p.exists(), str(p)
 hashes[a]=sha(p)
 for raw in re.findall(rb'[ -~]{5,}',p.read_bytes()):
  value=raw.decode('ascii')
  if re.fullmatch(r'/Game/[A-Za-z0-9_/\-]+',value): pending.append(value)
for name in ['SourceCopy','Stage']:
 d=work/name; (d/'Content').mkdir(parents=True)
 (d/(name+'.uproject')).write_text(json.dumps({'FileVersion':3,'EngineAssociation':'5.8','Plugins':[{'Name':n,'Enabled':True} for n in ['PythonScriptPlugin','EditorScriptingUtilities','Niagara']]},indent=2))
for a in sorted(seen):
 rel=Path(a[6:]+'.uasset'); dest=work/'SourceCopy'/'Content'/rel
 dest.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(source/'Content'/rel,dest)
 assert sha(dest)==hashes[a]
manifest={'project':str(project),'source':str(source),'work':str(work),'backup':str(backup),'roots':roots,'source_hashes':hashes,'backup_files':len(before)}
(work/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'work':str(work),'backup':str(backup),'backup_files':len(before),'isolated_packages':len(seen)}))
