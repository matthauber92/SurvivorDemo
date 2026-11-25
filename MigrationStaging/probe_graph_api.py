import unreal,json
from pathlib import Path
data={}
for cls in [unreal.BlueprintGraphEditor,unreal.K2Node_CustomEvent,unreal.BlueprintEditorLibrary]:
    data[cls.__name__]={n:str(getattr(cls,n).__doc__) for n in dir(cls) if not n.startswith('_')}
(Path(unreal.Paths.project_saved_dir())/'InteractionValidation/graph-api.json').write_text(json.dumps(data,indent=2))
