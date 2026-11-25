"""Apply closer camera defaults without rebuilding character or item attachments."""
import datetime
import shutil
from pathlib import Path
import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A

assert not unreal.EditorLevelLibrary.get_pie_worlds(False), 'Stop Play before applying camera defaults.'
path = '/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter'
root = Path(unreal.Paths.project_dir()).resolve()
bp = unreal.load_asset(path)
assert bp is not None
assert bp.get_editor_property('status') != unreal.BlueprintStatus.BS_ERROR, 'Repair Blueprint errors first.'
backup = root / 'Backups' / ('BeforeCloserCamera-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
backup.mkdir(parents=True)
shutil.copy2(root / 'Content' / (path[6:] + '.uasset'), backup / 'BP_SurvivorInteractionCharacter.uasset')
defaults = B.get_default_object(bp)
values = {'CameraWalkDistance': 250.0, 'CameraSprintDistance': 350.0,
          'CameraHipFireDistance': 220.0, 'CameraAimDistance': 180.0}
for name in values:
    defaults.get_editor_property(name)
boom = next(c for c in A.get_components(defaults) if c.get_name() == 'ShoulderBoom_GEN_VARIABLE')
for name, value in values.items():
    defaults.set_editor_property(name, value)
boom.set_editor_property('target_arm_length', values['CameraWalkDistance'])
assert unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
for name, value in values.items():
    assert abs(defaults.get_editor_property(name) - value) < 0.01
print('Saved closer camera defaults:', values)
