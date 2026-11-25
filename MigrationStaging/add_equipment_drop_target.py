import unreal,ast,toolset_registry
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B,_BlueprintCache
R='/Game/AIExample/UI/';ui=unreal.load_asset(R+'WBP_Inventory');op=unreal.load_asset(R+'BP_InventoryDragOperation')
with toolset_registry.tool_raising_exceptions():
 if 'ExpectedInstance' not in B.list_variables(op):B.add_variable(op,'ExpectedInstance','string')
 B.compile_blueprint(op)
_BlueprintCache.invalidate(ui)
# Keep the existing cursor-following drag visual; add a stable weapon identity
# to its payload rather than resolving a potentially changed slot on drop.
source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_inventory_drag_ui.py').read_text())
code=next(ast.literal_eval(n.args[2]) for n in ast.walk(source) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='write' and isinstance(n.args[1],ast.Constant) and n.args[1].value=='OnDragDetected')
code=code.replace('(bind Drag (UserInterface|CreateDrag&DropOperation','''(CallFunction|ClearCursorDragVisual)
  (Variables|Default|SetCursorDragVisual Visual)
  (UserInterface|Viewport|SetAlignmentinViewport :self Visual :Alignment (Math|Vector2D|MakeVector2D 0.5 0.5))
  (UserInterface|Viewport|SetDesiredSizeinViewport :self Visual :Size (Math|Vector2D|MakeVector2D 180.0 110.0))
  (CallFunction|PositionCursorDragVisual :ScreenPosition (Input|PointerEvent|GetScreenSpacePosition PointerEvent))
  (UserInterface|Viewport|AddtoViewport :self Visual :ZOrder 1000)
  (bind Proxy (UserInterface|CreateWidget :Class "/Game/AIExample/UI/WBP_InventoryDragProxy.WBP_InventoryDragProxy_C" :OwningPlayer (Widget|GetOwningPlayer)))
  (bind Drag (UserInterface|CreateDrag&DropOperation''').replace(':DefaultDragVisual Visual :Pivot "MouseDown"',':DefaultDragVisual Proxy :Pivot "CenterCenter"')
code=code.replace('(Class|BPInventoryDragOperation|SetSourceSlot', '''(bind Instance (Class|BPInventoryComponent|GetInstanceAtLocation :self (Variables|Default|GetInventorySource) :Location Slot))
  (Class|BPInventoryDragOperation|SetExpectedInstance :self Drag :ExpectedInstance Instance)
  (Variables|Default|SetSelectedLocation -1)
  (Variables|Default|SetSelectedInstance "")
  (Class|BPInventoryDragOperation|SetSourceSlot''')
with toolset_registry.tool_raising_exceptions():B.write_graph_dsl(B.get_graph(ui,'OnDragDetected'),code)
drop='''(fn OnDrop (MyGeometry PointerEvent Operation)
 (CallFunction|ClearCursorDragVisual)
 (CallFunction|RefreshInventory)
 (bind Drag (Utilities|Casting|CastToBP_InventoryDragOperation :Object Operation)
  (:then
   (if (== (Class|BPInventoryDragOperation|GetSourceWidget Drag) self)
    (bind PC (Utilities|Casting|CastToBP_InventoryPlayerController (Widget|GetOwningPlayer)))
    (bind Equipment (CallFunction|FindEquipmentAtPosition :Position (Input|PointerEvent|GetScreenSpacePosition PointerEvent)))
    (if (>= Equipment 8)
     (Class|BPInventoryPlayerController|RequestEquipmentTransfer :self PC
      :SourceLocation (Class|BPInventoryDragOperation|GetSourceSlot Drag) :TargetLocation Equipment
      :ExpectedInstance (Class|BPInventoryDragOperation|GetExpectedInstance Drag)
      :ExpectedVersion (Class|BPInventoryDragOperation|GetExpectedLayoutVersion Drag))
     (return true))
    (bind Target (CallFunction|FindSlotAtPosition :Position (Input|PointerEvent|GetScreenSpacePosition PointerEvent)))
    (if (>= Target 0)
     (Class|BPInventoryPlayerController|RequestMoveInventory :self PC
      :SourceSlot (Class|BPInventoryDragOperation|GetSourceSlot Drag) :TargetSlot Target
      :ExpectedID (Class|BPInventoryDragOperation|GetExpectedID Drag)
      :ExpectedQuantity (Class|BPInventoryDragOperation|GetExpectedQuantity Drag)
      :ExpectedLayoutVersion (Class|BPInventoryDragOperation|GetExpectedLayoutVersion Drag))
     (return true)))
   (return false))
  (:CastFailed (return false))))'''
with toolset_registry.tool_raising_exceptions():B.write_graph_dsl(B.get_graph(ui,'OnDrop'),drop)
tree=unreal.find_object(ui,'WidgetTree');unreal.find_object(tree,'CloseHint').set_text('DRAG BACKPACK ITEMS TO MOVE / EQUIP     [ I ] / [ ESC ] CLOSE')
for bp in [op,ui]:
 with toolset_registry.tool_raising_exceptions():B.compile_blueprint(bp,warnings_as_errors=True)
 assert bp.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE
 assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
print('EQUIPMENT_DROP_TARGET_SAVED')
