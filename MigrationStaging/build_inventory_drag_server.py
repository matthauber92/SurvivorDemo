import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B,ContainerType
R='/Game/AIExample/';inv=unreal.load_asset(R+'Items/BP_InventoryComponent');pc=unreal.load_asset(R+'Items/BP_InventoryPlayerController');ui=unreal.load_asset(R+'UI/WBP_Inventory')
def var(b,n,t,array=False):
 if n in B.list_variables(b):return
 if isinstance(t,str):B.add_variable(b,n,t,container_type=ContainerType.ARRAY if array else None)
 else:B.add_object_variable(b,n,t,container_type=ContainerType.ARRAY if array else None)
def fn(b,n,ins=[],outs=[]):
 g=B.get_graph(b,n)
 if g:return g
 g=B.add_function_graph(b,n)
 for name,typ in ins:B.add_function_param(g,name,typ,True)
 for name,typ in outs:B.add_function_param(g,name,typ,False)
 return g
def write(b,n,s):
 g=B.get_graph(b,n) or B.add_function_graph(b,n);B.write_graph_dsl(g,s)
 assert b.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE,(n,b.get_editor_property('status'))
var(inv,'SlotOrder','int',True);var(inv,'LayoutVersion','int')
for n in ['SlotOrder','LayoutVersion']:B.set_variable_replication(inv,n,unreal.BlueprintVariableReplication.REP_NOTIFY)
B.compile_blueprint(inv);unreal.get_default_object(inv.generated_class()).set_editor_property('SlotOrder',list(range(8)))
for n in ['SlotOrder','LayoutVersion']:write(inv,'OnRep_'+n,'(fn OnRep_'+n+' () (CallFunction|NotifyInventoryChanged))')
args=[('SourceSlot','int'),('TargetSlot','int'),('ExpectedID','name'),('ExpectedQuantity','int'),('ExpectedLayoutVersion','int')]
fn(inv,'TryMoveSlot',args,[('Moved','bool')])
write(inv,'TryMoveSlot','''(fn TryMoveSlot (SourceSlot TargetSlot ExpectedID ExpectedQuantity ExpectedLayoutVersion)
 (if (Networking|HasAuthority :self (Components|GetOwner))
  (if (and (and (>= SourceSlot 0) (< SourceSlot 8)) (and (>= TargetSlot 0) (< TargetSlot 8)))
   (if (and (!= SourceSlot TargetSlot) (== ExpectedLayoutVersion (Variables|Default|GetLayoutVersion)))
    (if (== (Utilities|Array|Length (Variables|Default|GetSlotOrder)) 8)
     (bind Index (Utilities|Array|Get(acopy) (Variables|Default|GetSlotOrder) SourceSlot))
     (if (and (Utilities|Array|IsValidIndex (Variables|Default|GetItemIDs) Index) (Utilities|Array|IsValidIndex (Variables|Default|GetQuantities) Index))
      (if (and (== (Utilities|Array|Get(acopy) (Variables|Default|GetItemIDs) Index) ExpectedID) (== (Utilities|Array|Get(acopy) (Variables|Default|GetQuantities) Index) ExpectedQuantity))
       (Utilities|Array|SwapArrayElements (Variables|Default|GetSlotOrder) SourceSlot TargetSlot)
       (Variables|Default|SetLayoutVersion (+ (Variables|Default|GetLayoutVersion) 1))
       (CallFunction|NotifyInventoryChanged)
       (return true)))))))
 (return false))''')
# Reuse a custom-event signature created with the Blueprint dispatcher API.
e=next(n for n in B.find_nodes(B.get_graph(pc,'EventGraph')) if isinstance(n,unreal.K2Node_CustomEvent) and 'MoveSlotSignature' in B._get_node_info(n).type_id)
asset=unreal.ConsoleVariablesAsset()
for prop,value in [('CustomFunctionName','ServerMoveInventory'),('FunctionFlags','203555008')]:
 d=unreal.ConsoleVariablesEditorAssetSaveData();d.import_text('(CommandName="set '+e.get_path_name()+' '+prop+'",CommandValueAsString="'+value+'",CheckedState=Checked)');asset.add_or_set_console_object_saved_data(d)
asset.execute_saved_commands(unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world());B.compile_blueprint(pc)
g=B.get_graph(pc,'EventGraph');call=B.create_node(g,'Class|BPInventoryComponent|TryMoveSlot',unreal.IntPoint(600,1000));getter=B.create_node(g,'Variables|Default|GetInventoryComponent',unreal.IntPoint(350,1300))
ei=B._get_node_info(e);ci=B._get_node_info(call)
for p in ci.input_pins:
 if p.name=='execute':B.connect_pins(next(x.pin_id for x in ei.output_pins if x.name=='then'),p.pin_id)
 elif p.name=='self':B.connect_pins(B._get_node_info(getter).output_pins[0].pin_id,p.pin_id)
 elif any(x.name==p.name for x in ei.output_pins):B.connect_pins(next(x.pin_id for x in ei.output_pins if x.name==p.name),p.pin_id)
B.remove_function_graph(pc,'MoveSlotSignature')
# Payload stores the originating widget and optimistic concurrency snapshot, never item data mutations.
f=unreal.BlueprintFactory();f.set_editor_property('parent_class',unreal.DragDropOperation)
op=unreal.load_asset(R+'UI/BP_InventoryDragOperation') or unreal.AssetToolsHelpers.get_asset_tools().create_asset('BP_InventoryDragOperation',R+'UI',unreal.Blueprint,f)
for n,t in args:
 if n!='TargetSlot':var(op,n,t)
var(op,'SourceWidget',ui.generated_class())
var(ui,'SlotFrames',unreal.Border.static_class(),True)
for n,t in [('DragSourceSlot','int'),('DragExpectedID','name'),('DragExpectedQuantity','int'),('DragExpectedLayoutVersion','int')]:var(ui,n,t)
if 'DragKey' not in B.list_variables(ui):B.add_struct_variable(ui,'DragKey',unreal.load_object(None,'/Script/InputCore.Key'))
fn(ui,'FindSlotAtPosition',[('Position','Vector2D')],[('SlotIndex','int')])
for b in [inv,pc,op,ui]:B.compile_blueprint(b)
key=unreal.Key();key.import_text('LeftMouseButton');unreal.get_default_object(ui.generated_class()).set_editor_property('DragKey',key)
for b in [inv,pc,op]:unreal.EditorAssetLibrary.save_loaded_asset(b)
g=B.get_graph(ui,'EventGraph')
for term in ['UserInterface|CreateDrag&DropOperation','Widget|DragandDrop|EventReply|DetectDragifPressed','UserInterface|Geometry|IsUnderLocation','Input|PointerEvent|GetScreenSpacePosition']:
 print(term,[(p.name,p.type_id) for p in B.get_node_type_pins(g,term).input_pins])
print('OP_EVENTS',[str(x.name) for x in B.list_events(op)])
print('RPC_READY',B._get_node_info(e).type_id)
