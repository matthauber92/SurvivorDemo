import unreal
import json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools

project = Path(unreal.Paths.project_dir()).resolve()
assert project.name == 'GASP-20261117-054307'
out = project / 'BlueprintInspection'
out.mkdir(exist_ok=True)
for name in ['SandboxCharacter_CMC', 'AC_VisualOverrideManager', 'PC_Sandbox', 'GM_Sandbox']:
    bp = unreal.load_asset('/Game/Blueprints/' + name)
    graphs = BlueprintTools.list_graphs(bp)
    for graph in graphs:
        try:
            (out / (name + '__' + graph.get_name() + '.txt')).write_text(BlueprintTools.read_graph_dsl(graph), encoding='utf-8')
        except Exception as exc:
            unreal.log_warning(str(exc))
    cdo = unreal.get_default_object(bp.generated_class())
    (out / (name + '__properties.txt')).write_text(str(cdo), encoding='utf-8')
unreal.log('BLUEPRINT_INSPECTION_COMPLETE')
