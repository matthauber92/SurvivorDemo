import unreal, json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out = Path(unreal.Paths.project_saved_dir())/'InteractionValidation'
out.mkdir(exist_ok=True)
data = {}
for cls in [unreal.BlueprintEditorLibrary, unreal.K2Node_CustomEvent]:
    data[cls.__name__] = {x:str(getattr(cls,x).__doc__) for x in dir(cls) if any(s in x.lower() for s in ['interface','replic','event','param','function_flag'])}
bp = unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC')
data['graphs'] = [g.get_name() for g in B.list_graphs(bp)]
for name in ['EventGraph','SetupInput']:
    try: data[name] = B.read_graph_dsl(B.get_graph(bp,name))
    except Exception as e: data[name] = str(e)
data['input'] = str(unreal.load_asset('/Game/Input/IMC_Sandbox').get_editor_property('mappings'))
(out/'architecture.json').write_text(json.dumps(data,indent=2))
print('Architecture saved')
