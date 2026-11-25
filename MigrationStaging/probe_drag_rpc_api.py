import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
print('LIB',[n for n in dir(unreal.BlueprintEditorLibrary) if any(t in n for t in ['param','pin','event'])])
print('GRAPH',[n for n in dir(unreal.BlueprintGraphEditor) if any(t in n for t in ['pin','import','event'])])
print('NODE',[n for n in dir(unreal.K2Node_EditablePinBase) if 'pin' in n])
b=unreal.load_asset('/Game/AIExample/UI/WBP_Inventory');g=B.get_graph(b,'EventGraph')
for term in ['CreateDrag','ConstructObject','SetDragVisual']:
 print(term,list(B.find_node_types(g,term,[])))
