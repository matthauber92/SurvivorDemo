import unreal
import json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools
from editor_toolset.toolsets.actor import ActorTools

project = Path(unreal.Paths.project_dir()).resolve()
assert project.name == 'GASP-20261117-054307'
base = unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC')
cdo = unreal.get_default_object(base.generated_class())
removed = []
for component in ActorTools.get_components(cdo):
    if 'AC_VisualOverrideManager' in component.get_class().get_path_name():
        removed.append(component.get_path_name())
        assert ActorTools.remove_component(component)
assert len(removed) <= 1
BlueprintTools.compile_blueprint(base)
assert unreal.EditorAssetLibrary.save_loaded_asset(base)
# Replace only the new staging asset made by prepare_foundation.py. Inherit the
# CMC base so its pre-movement tick helper's base-class cast remains valid.
destination = '/Game/AIExample/Gameplay/Characters/BP_SurvivorCharacter'
assert (project / 'foundation-preparation.json').exists()
assert not unreal.EditorAssetLibrary.does_asset_exist(destination), 'Expected prior staging draft deletion to have completed'
factory = unreal.BlueprintFactory()
factory.set_editor_property('parent_class', base.generated_class())
bp = unreal.AssetToolsHelpers.get_asset_tools().create_asset('BP_SurvivorCharacter', '/Game/AIExample/Gameplay/Characters', unreal.Blueprint, factory)
assert bp
BlueprintTools.compile_blueprint(bp)
cdo = unreal.get_default_object(bp.generated_class())
cdo.set_editor_property('replicates', True)
cdo.set_editor_property('replicate_movement', True)
assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
(project / 'foundation-preparation.json').write_text(json.dumps(dict(character=destination,parent='/Game/Blueprints/SandboxCharacter_CMC',removed_showcase_component=removed,reason='Preserve base-class compatibility with GASP pre-CMC tick helper'),indent=2))
unreal.log('FOUNDATION_REFINED')
exec((Path(__file__).resolve().parent / 'migrate_foundation.py').read_text())
