import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionTestDoor')
g=B.get_graph(bp,'OnRep_IsOpen')
print('TYPES',list(B.find_node_types(g,'Branch',[])),list(B.find_node_types(g,'SetRelativeRotation',[])))
print('HINGE_TYPES',list(B.find_node_types(g,'DoorHinge',[])))
for t in ['Utilities|FlowControl|Branch','Transformation|SetRelativeRotation','Variables|Components|GetDoorHinge','Variables|Default|GetIsOpen']:
    print('PINS',t,B.get_node_type_pins(g,t))
