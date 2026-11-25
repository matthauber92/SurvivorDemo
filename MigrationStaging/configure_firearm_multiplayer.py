import unreal,json
from pathlib import Path
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.LevelEditorPlaySettings'))
props=['PlayNumberOfClients','PlayNetMode','RunUnderOneProcess']
p=Path(unreal.Paths.project_saved_dir())/'firearm-play-settings.json'
if not p.exists():p.write_text(json.dumps({k:(0 if k=='PlayNetMode' else s.get_editor_property(k)) for k in props}))
from editor_toolset.toolsets.object import ObjectTools as O
print('NETMODE_SCHEMA',json.loads(O.list_properties(s)).get('playNetMode'))
assert O.set_properties(s,json.dumps({'PlayNumberOfClients':2,'PlayNetMode':'PIE_ListenServer','RunUnderOneProcess':True}))
