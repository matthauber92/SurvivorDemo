import unreal,json
from pathlib import Path
from editor_toolset.toolsets.object import ObjectTools as O
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.LevelEditorPlaySettings'))
p=Path(unreal.Paths.project_saved_dir())/'firearm-play-settings.json';data=json.loads(p.read_text());data['PlayNetMode']=['PIE_Standalone','PIE_ListenServer','PIE_Client'][data['PlayNetMode']]
assert O.set_properties(s,json.dumps(data));print('RESTORED_PLAY_SETTINGS',data)
