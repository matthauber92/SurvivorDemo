import unreal,inspect,json
from editor_toolset.toolsets.blueprint import BlueprintTools as B
print('WIDGET_API', [n for n in dir(unreal) if any(t in n for t in ['WidgetBlueprint','WidgetTree','ToolsetLibrary'])])
for cls in ['WidgetBlueprint','WidgetBlueprintLibrary','WidgetTree','ToolsetLibrary']:
 c=getattr(unreal,cls,None)
 if c: print(cls,[n for n in dir(c) if any(t in n.lower() for t in ['widget','construct','function','property','root'])])
print('B_FILE',inspect.getfile(B))
for path in ['/Game/AIExample/Items/BP_InventoryPlayerController','/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter']:
 b=unreal.load_asset(path)
 print(path,{g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(b)})
print('WORLD',unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world().get_name())
