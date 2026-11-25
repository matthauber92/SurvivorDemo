import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/UI/BP_InventoryDragOperation')
g=B.get_graph(bp,'EventGraph')
for term in ['AbsoluteToViewport','SetPositioninViewport','SetAlignmentinViewport','AddtoViewport','EventDragged','EventDrop','RemovefromParent','MakeVector2D']:
 print(term,list(B.find_node_types(g,term,[])))
for term in ['UserInterface|Geometry|AbsolutetoViewport','UserInterface|Viewport|SetPositioninViewport','UserInterface|Viewport|AddtoViewport']:
 p=B.get_node_type_pins(g,term)
 print(term,[(x.name,x.type_id) for x in p.input_pins],[(x.name,x.type_id) for x in p.output_pins])
import inspect
print(inspect.getsource(B.add_function_param))
