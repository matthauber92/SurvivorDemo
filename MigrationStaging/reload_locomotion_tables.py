import unreal,json
from pathlib import Path
paths=json.loads((Path(unreal.Paths.project_saved_dir())/'ShoulderCamera/repaired-animation-contexts.json').read_text())
packages=[unreal.load_asset(p).get_outermost() for p in paths]
print('MODES',list(unreal.ReloadPackagesInteractionMode))
print(unreal.EditorLoadingAndSavingUtils.reload_packages(packages,unreal.ReloadPackagesInteractionMode.ASSUME_POSITIVE))
