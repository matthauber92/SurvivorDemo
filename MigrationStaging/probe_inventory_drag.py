import unreal,json
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/UI/WBP_Inventory')
for n in ['OnPreviewMouseButtonDown','OnDragDetected','OnDrop','OnDragCancelled']:
 g=B.add_function_graph(b,n);print(n,B.read_graph_dsl(g))
g=B.get_graph(b,'EventGraph')
for term in ['DetectDrag','DragDrop','ScreenSpacePosition','IsUnderLocation','GetCachedGeometry','GetEffectingButton','CancelDrag','SwapArray','CreateEvent']:
 print(term,list(B.find_node_types(g,term,[])))
print('CUSTOM', [n for n in dir(unreal.K2Node_CustomEvent) if any(x in n for x in ['pin','flag','replic'])])
