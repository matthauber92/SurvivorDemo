import unreal
import json
import hashlib
from pathlib import Path

project = Path(unreal.Paths.project_dir()).resolve()
assert project.name == 'GASP-20261117-054307'
exec((Path(__file__).resolve().parent / 'inspect_gasp.py').read_text())
report = json.loads((project / 'dependency-report.json').read_text())
assert not report['conflicts'], report['conflicts']
assert not report['missing'], report['missing']
assert '/Game/Blueprints/GM_Sandbox' not in report['packages'], 'Showcase GameMode still referenced'
assert not any(p.startswith('/Game/MetaHumans/') for p in report['packages']), 'Unexpected early MetaHuman dependency'
target = Path(__file__).resolve().parents[1] / 'Content'
def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()
before = {str(p.relative_to(target)): sha(p) for p in target.rglob('*') if p.is_file()}
(project / 'destination-before-migration.json').write_text(json.dumps(before, indent=2))
options = unreal.MigrationOptions()
options.set_editor_property('prompt', False)
options.set_editor_property('ignore_dependencies', False)
options.set_editor_property('asset_conflict', unreal.AssetMigrationConflict.SKIP)
unreal.AssetToolsHelpers.get_asset_tools().migrate_packages(report['roots'], str(target), options)
changed = [p for p, digest in before.items() if not (target/p).exists() or sha(target/p) != digest]
missing = [p for p in report['packages'] if not any((target/(p[len('/Game/'):] + ext)).exists() for ext in ('.uasset','.umap'))]
result = dict(api='unreal.AssetTools.migrate_packages', package_count=len(report['packages']), existing_files_changed=changed, missing_packages=missing)
(project / 'migration-result.json').write_text(json.dumps(result, indent=2))
assert not changed, changed
assert not missing, 'Migration incomplete: ' + str(len(missing)) + ' packages missing; see migration-result.json'
unreal.log('MIGRATION_VERIFIED ' + json.dumps(result))
