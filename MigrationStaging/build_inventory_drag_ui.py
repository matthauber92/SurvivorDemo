import unreal,ast
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B,_BlueprintCache
R='/Game/AIExample/';ui=unreal.load_asset(R+'UI/WBP_Inventory');pc=unreal.load_asset(R+'Items/BP_InventoryPlayerController');op=unreal.load_asset(R+'UI/BP_InventoryDragOperation')
for b in [ui,pc,op]:_BlueprintCache.invalidate(b)
def write(b,n,code):
 g=B.get_graph(b,n) or B.add_function_graph(b,n);B.write_graph_dsl(g,code)
 print('WRITE',b.get_name(),n,b.get_editor_property('status'))
source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_inventory_ui_logic.py').read_text())
for node in ast.walk(source):
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='write' and isinstance(node.args[1],ast.Constant):
  n=node.args[1].value
  if n=='CacheSlotWidgets':
   s=ast.literal_eval(node.args[2]).replace('(fn CacheSlotWidgets ()','(fn CacheSlotWidgets () (Utilities|Array|Clear (Variables|Default|GetSlotFrames))').replace('(bind Contents','(Utilities|Array|Add (Variables|Default|GetSlotFrames) Slot)\n  (bind Contents')
   write(ui,n,s)
  elif n=='RefreshInventory' and isinstance(node.args[0],ast.Name) and node.args[0].id=='ui':
   s=ast.literal_eval(node.args[2]).replace('(if (< i Count)','(Widget|SetRenderOpacity (Utilities|Array|Get(acopy) (Variables|Default|GetSlotFrames) i) 1.0)\n    (bind StorageIndex (Utilities|Array|Get(acopy) (Class|BPInventoryComponent|GetSlotOrder (Variables|Default|GetInventorySource)) i))\n    (if (< StorageIndex Count)').replace('Get(acopy) IDs i','Get(acopy) IDs StorageIndex').replace('Get(acopy) Quantities i','Get(acopy) Quantities StorageIndex')
   write(ui,n,s)
  elif n=='CloseInventory':
   s=ast.literal_eval(node.args[2]).replace('(Variables|Default|SetInventoryOpen false)','(Widget|DragandDrop|CancelDragDrop)\n  (Variables|Default|SetInventoryOpen false)')
   write(pc,n,s)
write(ui,'FindSlotAtPosition','''(fn FindSlotAtPosition (Position)
 (for i (range (Utilities|Array|Length (Variables|Default|GetSlotFrames)))
  (if (UserInterface|Geometry|IsUnderLocation (Widget|GetCachedGeometry (Utilities|Array|Get(acopy) (Variables|Default|GetSlotFrames) i)) Position)
   (return i)))
 (return -1))''')
write(ui,'OnPreviewMouseButtonDown','''(fn OnPreviewMouseButtonDown (MyGeometry MouseEvent)
 (Variables|Default|SetDragSourceSlot -1)
 (if (== (Input|PointerEvent|GetEffectingButton MouseEvent) (Variables|Default|GetDragKey))
  (bind Slot (CallFunction|FindSlotAtPosition :Position (Input|PointerEvent|GetScreenSpacePosition MouseEvent)))
  (if (>= Slot 0)
   (bind Inv (Variables|Default|GetInventorySource))
   (bind Index (Utilities|Array|Get(acopy) (Class|BPInventoryComponent|GetSlotOrder Inv) Slot))
   (if (and (Utilities|Array|IsValidIndex (Class|BPInventoryComponent|GetItemIDs Inv) Index) (Utilities|Array|IsValidIndex (Class|BPInventoryComponent|GetQuantities Inv) Index))
    (Variables|Default|SetDragSourceSlot Slot)
    (Variables|Default|SetDragExpectedID (Utilities|Array|Get(acopy) (Class|BPInventoryComponent|GetItemIDs Inv) Index))
    (Variables|Default|SetDragExpectedQuantity (Utilities|Array|Get(acopy) (Class|BPInventoryComponent|GetQuantities Inv) Index))
    (Variables|Default|SetDragExpectedLayoutVersion (Class|BPInventoryComponent|GetLayoutVersion Inv))
    (bind Reply (Widget|DragandDrop|EventReply|DetectDragifPressed :PointerEvent MouseEvent :DragKey (Variables|Default|GetDragKey))) (return Reply))))
 (return (Widget|EventReply|Unhandled)))''')
write(ui,'OnDragDetected','''(fn OnDragDetected (MyGeometry PointerEvent)
 (if (>= (Variables|Default|GetDragSourceSlot) 0)
  (bind Slot (Variables|Default|GetDragSourceSlot))
  (bind Visual (UserInterface|CreateWidget :Class "/Game/AIExample/UI/WBP_InventoryDragVisual.WBP_InventoryDragVisual_C" :OwningPlayer (Widget|GetOwningPlayer)))
  (Class|WBPInventoryDragVisual|SetDragTitle :self Visual :DragTitle (Widget|GetText(Text) (Utilities|Array|Get(acopy) (Variables|Default|GetNameLabels) Slot)))
  (Class|WBPInventoryDragVisual|SetDragCount :self Visual :DragCount (Widget|GetText(Text) (Utilities|Array|Get(acopy) (Variables|Default|GetQuantityLabels) Slot)))
  (Class|WBPInventoryDragVisual|SetDragTexture :self Visual :DragTexture (Widget|Brush|GetBrushResourceasTexture2D (Class|Border|GetBrush (Utilities|Array|Get(acopy) (Variables|Default|GetIconFrames) Slot))))
  (bind Drag (UserInterface|CreateDrag&DropOperation :Class "/Game/AIExample/UI/BP_InventoryDragOperation.BP_InventoryDragOperation_C" :DefaultDragVisual Visual :Pivot "MouseDown"))
  (Class|BPInventoryDragOperation|SetSourceWidget :self Drag :SourceWidget self)
  (Class|BPInventoryDragOperation|SetSourceSlot :self Drag :SourceSlot Slot)
  (Class|BPInventoryDragOperation|SetExpectedID :self Drag :ExpectedID (Variables|Default|GetDragExpectedID))
  (Class|BPInventoryDragOperation|SetExpectedQuantity :self Drag :ExpectedQuantity (Variables|Default|GetDragExpectedQuantity))
  (Class|BPInventoryDragOperation|SetExpectedLayoutVersion :self Drag :ExpectedLayoutVersion (Variables|Default|GetDragExpectedLayoutVersion))
  (Widget|SetRenderOpacity (Utilities|Array|Get(acopy) (Variables|Default|GetSlotFrames) Slot) 0.4)
  (return Drag))
 (return "None"))''')
write(ui,'OnDrop','''(fn OnDrop (MyGeometry PointerEvent Operation)
 (CallFunction|RefreshInventory)
 (bind Drag (Utilities|Casting|CastToBP_InventoryDragOperation :Object Operation)
  (:then
   (if (== (Class|BPInventoryDragOperation|GetSourceWidget Drag) self)
    (bind Target (CallFunction|FindSlotAtPosition :Position (Input|PointerEvent|GetScreenSpacePosition PointerEvent)))
    (if (>= Target 0)
     (bind PC (Utilities|Casting|CastToBP_InventoryPlayerController (Widget|GetOwningPlayer)))
     (Class|BPInventoryPlayerController|RequestMoveInventory :self PC
      :SourceSlot (Class|BPInventoryDragOperation|GetSourceSlot Drag) :TargetSlot Target
      :ExpectedID (Class|BPInventoryDragOperation|GetExpectedID Drag)
      :ExpectedQuantity (Class|BPInventoryDragOperation|GetExpectedQuantity Drag)
      :ExpectedLayoutVersion (Class|BPInventoryDragOperation|GetExpectedLayoutVersion Drag))
     (return true)))
   (return false))
  (:CastFailed (return false))))''')
B.write_graph_dsl(B.get_graph(op,'EventGraph'),'''(event AddEvent|DragandDrop|EventDragCancelled (PointerEvent)
 (Utilities|IsValid (Variables|Default|GetSourceWidget)
  (:"Is Valid" (Class|WBPInventory|RefreshInventory (Variables|Default|GetSourceWidget)))
  (:"Is Not Valid")))''')
# Describe the gesture without introducing item use or world dropping.
t=unreal.find_object(ui,'WidgetTree');unreal.find_object(t,'CloseHint').set_text('DRAG TO MOVE / SWAP     [ I ] / [ ESC ] CLOSE')
for b in [ui,pc,op]:
 B.compile_blueprint(b,warnings_as_errors=True)
 assert b.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE,(b.get_name(),b.get_editor_property('status'))
 assert unreal.EditorAssetLibrary.save_loaded_asset(b)
print('DRAG_UI_SAVED')

