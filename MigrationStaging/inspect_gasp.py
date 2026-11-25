import unreal
import json
from pathlib import Path

project = Path(unreal.Paths.project_dir()).resolve()
assert project.name == 'GASP-20261117-054307', str(project)
registry = unreal.AssetRegistryHelpers.get_asset_registry()
registry.search_all_assets(True)
registry.scan_paths_synchronous(['/Game'], True)
options = unreal.AssetRegistryDependencyOptions()
character = '/Game/AIExample/Gameplay/Characters/BP_SurvivorCharacter' if (project / 'Content/AIExample/Gameplay/Characters/BP_SurvivorCharacter.uasset').exists() else '/Game/Blueprints/SandboxCharacter_CMC'
roots = [character, '/Game/Input/IMC_Sandbox']
pending = list(roots)
seen = set()
edges = {}
external = set()
while pending:
    package = pending.pop()
    if package in seen:
        continue
    seen.add(package)
    raw_deps = registry.get_dependencies(package, options)
    if raw_deps is None:
        raise RuntimeError('Registry did not return dependency information for ' + package)
    deps = sorted(str(x) for x in raw_deps)
    edges[package] = deps
    for dep in deps:
        if dep.startswith('/Game/'):
            if dep not in seen:
                pending.append(dep)
        else:
            external.add(dep)
destination = Path(__file__).resolve().parents[1] / 'Content'
conflicts = []
missing = []
for package in sorted(seen):
    relative = package[len('/Game/'):]
    files = [project / 'Content' / (relative + ext) for ext in ('.uasset', '.umap')]
    if not any(p.exists() for p in files):
        missing.append(package)
    for ext in ('.uasset', '.umap'):
        if (destination / (relative + ext)).exists():
            conflicts.append(package)
result = dict(roots=roots, packages=sorted(seen), external=sorted(external), edges=edges,
              conflicts=sorted(set(conflicts)), missing=missing,
              migration_api=hasattr(unreal.AssetToolsHelpers.get_asset_tools(), 'migrate_packages'))
(project / 'dependency-report.json').write_text(json.dumps(result, indent=2))
unreal.log('GASP_PREFLIGHT ' + json.dumps({k: v for k, v in result.items() if k not in ('edges','packages','external')}))
unreal.log('GASP_PACKAGE_COUNT ' + str(len(seen)))
