import unreal, json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
data={}
data['apis']=[n for n in dir(unreal) if any(s in n for s in ['Blueprint','GraphEditor','Interface'])]
data['custom_event_doc']=unreal.K2Node_CustomEvent.__doc__
data['blueprint_doc']=unreal.Blueprint.__doc__
bp=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC')
g=B.get_graph(bp,'EventGraph')
for n in B.find_nodes(g):
    if isinstance(n,unreal.K2Node_CustomEvent):
        d={'node':n.get_name()}
        for p in ['function_flags','custom_function_name']:
            try:d[p]=str(n.get_editor_property(p))
            except Exception as e:d[p]=str(e)
        data.setdefault('events',[]).append(d)
data['interface_doc']=unreal.BPInterfaceDescription.__doc__ if hasattr(unreal,'BPInterfaceDescription') else ''
data['E_binding']=[str(m) for m in unreal.load_asset('/Game/Input/IMC_Sandbox').get_editor_property('mappings') if str(m.key).find('E')>=0]
(Path(unreal.Paths.project_saved_dir())/'InteractionValidation/api.json').write_text(json.dumps(data,indent=2))
