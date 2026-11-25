import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionTestDoor')
g=B.get_graph(bp,'OnRep_IsOpen')
print('BEFORE',B.read_graph_dsl(g))
B.write_graph_dsl(g,'''(fn OnRep_IsOpen ()
 (Transformation|SetRelativeRotation :self (Variables|Components|GetDoorHinge)
  :NewRotation (Math|Rotator|MakeRotator :Yaw (select (Variables|Default|GetIsOpen) 90.0 0.0))))''')
print('AFTER',B.read_graph_dsl(B.get_graph(bp,'OnRep_IsOpen')))
for n in B.find_nodes(B.get_graph(bp,'OnRep_IsOpen')):
    print('NODE',B._get_node_info(n))
unreal.EditorAssetLibrary.save_loaded_asset(bp)
import inspect
print(inspect.getsource(B.write_graph_dsl))
print(inspect.getsource(B.get_graph))
