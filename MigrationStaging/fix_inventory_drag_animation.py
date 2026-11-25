import unreal,ast
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B,_BlueprintCache
root='/Game/AIExample/UI/'
ui=unreal.load_asset(root+'WBP_Inventory')
op=unreal.load_asset(root+'BP_InventoryDragOperation')
proxy=unreal.load_asset(root+'WBP_InventoryDragProxy') or unreal.EditorAssetLibrary.duplicate_asset(root+'WBP_InventoryDragVisual',root+'WBP_InventoryDragProxy')
# UMG still owns the drag payload/drop handling; its animated decorator is empty.
for graph in B.list_graphs(proxy):
 for node in list(B.find_nodes(graph)):B.delete_node(node)
tree=unreal.find_object(proxy,'WidgetTree')
unreal.find_object(tree,'Overlay_19').clear_children()
B.compile_blueprint(proxy,warnings_as_errors=True)
unreal.get_default_object(proxy.generated_class()).set_visibility(unreal.SlateVisibility.HIT_TEST_INVISIBLE)
unreal.EditorAssetLibrary.save_loaded_asset(proxy)
if 'CursorDragVisual' not in B.list_variables(ui):B.add_object_variable(ui,'CursorDragVisual',unreal.UserWidget.static_class())
g=B.get_graph(ui,'PositionCursorDragVisual') or B.add_function_graph(ui,'PositionCursorDragVisual')
if not B.get_graph(ui,'ClearCursorDragVisual'):
 B.add_function_param(g,'ScreenPosition','Vector2D',True)
 B.add_function_graph(ui,'ClearCursorDragVisual')
B.write_graph_dsl(g,'''(fn PositionCursorDragVisual (ScreenPosition)
 (Utilities|IsValid (Variables|Default|GetCursorDragVisual)
  (:"Is Valid"
   (bind (PixelPosition ViewportPosition) (UserInterface|Geometry|AbsolutetoViewport :AbsoluteDesktopCoordinate ScreenPosition))
   (UserInterface|Viewport|SetPositioninViewport :self (Variables|Default|GetCursorDragVisual) :Position PixelPosition :bRemoveDPIScale true))
  (:"Is Not Valid")))''')
B.write_graph_dsl(B.get_graph(ui,'ClearCursorDragVisual'),'''(fn ClearCursorDragVisual ()
 (Utilities|IsValid (Variables|Default|GetCursorDragVisual)
  (:"Is Valid" (Widget|RemovefromParent (Variables|Default|GetCursorDragVisual)) (Variables|Default|SetCursorDragVisual "None"))
  (:"Is Not Valid")))''')
B.compile_blueprint(ui,warnings_as_errors=True)
_BlueprintCache.invalidate(op)
B.write_graph_dsl(B.get_graph(op,'EventGraph'),'''(event AddEvent|DragandDrop|EventDragged (PointerEvent)
 (Utilities|IsValid (Variables|Default|GetSourceWidget)
  (:"Is Valid" (Class|WBPInventory|PositionCursorDragVisual :self (Variables|Default|GetSourceWidget) :ScreenPosition (Input|PointerEvent|GetScreenSpacePosition PointerEvent)))
  (:"Is Not Valid")))
(event AddEvent|DragandDrop|EventDragCancelled (PointerEvent)
 (Utilities|IsValid (Variables|Default|GetSourceWidget)
  (:"Is Valid" (Class|WBPInventory|ClearCursorDragVisual (Variables|Default|GetSourceWidget)) (Class|WBPInventory|RefreshInventory (Variables|Default|GetSourceWidget)))
  (:"Is Not Valid")))
(event AddEvent|DragandDrop|EventDrop (PointerEvent)
 (Utilities|IsValid (Variables|Default|GetSourceWidget)
  (:"Is Valid" (Class|WBPInventory|ClearCursorDragVisual (Variables|Default|GetSourceWidget)))
  (:"Is Not Valid")))''')
source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_inventory_drag_ui.py').read_text())
for node in ast.walk(source):
 if not (isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='write' and len(node.args)>2 and isinstance(node.args[1],ast.Constant)):continue
 name=node.args[1].value
 if name=='OnDragDetected':
  code=ast.literal_eval(node.args[2])
  code=code.replace('(bind Drag (UserInterface|CreateDrag&DropOperation', '''(CallFunction|ClearCursorDragVisual)
  (Variables|Default|SetCursorDragVisual Visual)
  (UserInterface|Viewport|SetAlignmentinViewport :self Visual :Alignment (Math|Vector2D|MakeVector2D 0.5 0.5))
  (UserInterface|Viewport|SetDesiredSizeinViewport :self Visual :Size (Math|Vector2D|MakeVector2D 180.0 110.0))
  (CallFunction|PositionCursorDragVisual :ScreenPosition (Input|PointerEvent|GetScreenSpacePosition PointerEvent))
  (UserInterface|Viewport|AddtoViewport :self Visual :ZOrder 1000)
  (bind Proxy (UserInterface|CreateWidget :Class "/Game/AIExample/UI/WBP_InventoryDragProxy.WBP_InventoryDragProxy_C" :OwningPlayer (Widget|GetOwningPlayer)))
  (bind Drag (UserInterface|CreateDrag&DropOperation''').replace(':DefaultDragVisual Visual :Pivot "MouseDown"',':DefaultDragVisual Proxy :Pivot "CenterCenter"')
  B.write_graph_dsl(B.get_graph(ui,name),code)
 elif name=='OnDrop':
  code=ast.literal_eval(node.args[2]).replace('(CallFunction|RefreshInventory)','(CallFunction|ClearCursorDragVisual) (CallFunction|RefreshInventory)')
  B.write_graph_dsl(B.get_graph(ui,name),code)
for bp in [proxy,op,ui]:
 B.compile_blueprint(bp,warnings_as_errors=True)
 assert bp.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE,(bp.get_name(),bp.get_editor_property('status'))
 assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
print('DIRECT_CURSOR_VISUAL_SAVED')
