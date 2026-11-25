from pathlib import Path
import re,shutil,json
root=Path(__file__).resolve().parent.parent
src=Path(r'C:\Users\Matt Hauber\Documents\Unreal Projects\TheHouse\TheHouse 5.8')
dst=root/'MigrationStaging/HouseCameraReference';dst.mkdir(exist_ok=True)
pending=['/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter','/Game/SurvivalMan/Blueprints/BP_ThirdPersonCharacter'];seen=set();total=0
while pending:
 a=pending.pop()
 if a in seen:continue
 seen.add(a);p=src/'Content'/(a[6:]+'.uasset')
 if not p.exists():continue
 for raw in re.findall(rb'[ -~]{5,}',p.read_bytes()):
  v=raw.decode('ascii')
  if re.fullmatch(r'/Game/[A-Za-z0-9_/\-]+',v):pending.append(v)
 d=dst/'Content'/(a[6:]+'.uasset');d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);total+=p.stat().st_size
(dst/'HouseCameraReference.uproject').write_text(json.dumps({'FileVersion':3,'EngineAssociation':'5.8','Plugins':[{'Name':n,'Enabled':True} for n in ['PythonScriptPlugin','EditorScriptingUtilities','EditorToolset','Niagara']]}))
print({'files':len(seen),'bytes':total})
