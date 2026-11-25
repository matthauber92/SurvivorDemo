import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
pc=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController')
g=B.add_event_dispatcher(pc,'MoveSlotSignature')
for n,t in [('SourceSlot','int'),('TargetSlot','int'),('ExpectedID','name'),('ExpectedQuantity','int'),('ExpectedLayoutVersion','int')]:B.add_function_param(g,n,t,True)
B.compile_blueprint(pc)
e=unreal.BlueprintGraphEditor.get_graph_editor(B.get_graph(pc,'EventGraph')).add_dispatcher_event_node('MoveSlotSignature')
print('NODE',e,e.get_class().get_name());print(B._get_node_info(e))
