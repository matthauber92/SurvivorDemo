import unreal
import json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools
from editor_toolset.toolsets.actor import ActorTools

project = Path(unreal.Paths.project_dir()).resolve()
assert project.name == 'GASP-20261117-054307'
destination = '/Game/AIExample/Characters/BP_SurvivorCharacter'
assert not unreal.EditorAssetLibrary.does_asset_exist(destination), 'Refusing overwrite'
bp = unreal.EditorAssetLibrary.duplicate_asset('/Game/Blueprints/SandboxCharacter_CMC', destination)
assert bp
cdo = unreal.get_default_object(bp.generated_class())
components = ActorTools.get_components(cdo)
removed = []
for component in components:
    if 'AC_VisualOverrideManager' in component.get_class().get_path_name():
        removed.append(component.get_path_name())
        assert ActorTools.remove_component(component)
assert len(removed) == 1, str(removed)
BlueprintTools.compile_blueprint(bp)
cdo = unreal.get_default_object(bp.generated_class())
cdo.set_editor_property('replicates', True)
cdo.set_editor_property('replicate_movement', True)
assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
(project / 'foundation-preparation.json').write_text(json.dumps(dict(character=destination,removed_components=removed,components=[dict(name=c.get_name(),type=c.get_class().get_path_name()) for c in ActorTools.get_components(cdo)]),indent=2))
exec((Path(__file__).resolve().parent / 'inspect_gasp.py').read_text())
unreal.log('FOUNDATION_PREPARED')
