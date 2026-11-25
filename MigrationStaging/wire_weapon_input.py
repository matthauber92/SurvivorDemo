import unreal,toolset_registry
from editor_toolset.toolsets.blueprint import BlueprintTools as B,_BlueprintCache
R='/Game/AIExample/'
pc=unreal.load_asset(R+'Items/BP_InventoryPlayerController');g=B.get_graph(pc,'EventGraph')
def pin(n,name,out=False):return next(p.pin_id for p in (B._get_node_info(n).output_pins if out else B._get_node_info(n).input_pins) if p.name==name)
def fn(n,args=[]):
 result=next((x for x in B.list_graphs(pc) if x.get_name()==n),None)
 if not result:
  result=B.add_function_graph(pc,n)
  for k,t in args:B.add_function_param(result,k,t,True)
 return result
with toolset_registry.tool_raising_exceptions():
 event=next(n for n in B.find_nodes(g) if isinstance(n,unreal.K2Node_CustomEvent) and 'ServerSelectWeapon' in B._get_node_info(n).type_id)
 if not any(p.connected_pins for p in B._get_node_info(event).output_pins):
  call=B.create_node(g,'Class|BPInventoryComponent|TrySelectWeapon',unreal.IntPoint(600,2400))
  getter=B.create_node(g,'Variables|Default|GetInventoryComponent',unreal.IntPoint(350,2700))
  B.connect_pins(pin(event,'then',True),pin(call,'execute'))
  B.connect_pins(B._get_node_info(getter).output_pins[0].pin_id,pin(call,'self'))
  for n in ['Slot','ExpectedInstance','ExpectedVersion']:B.connect_pins(pin(event,n,True),pin(call,n))
 B.compile_blueprint(pc);_BlueprintCache.invalidate(pc)
 B.write_graph_dsl(fn('RequestSelectWeapon',[('Slot','int')]),'''(fn RequestSelectWeapon (Slot)
 (if (and (Pawn|IsLocalController) (not (Variables|Default|GetInventoryOpen)))
  (if (and (>= Slot 0) (< Slot 3))
   (CallFunction|ServerSelectWeapon :Slot Slot :ExpectedInstance (Class|BPInventoryComponent|GetInstanceAtLocation :self (Variables|Default|GetInventoryComponent) :Location (+ Slot 8)) :ExpectedVersion (Class|BPInventoryComponent|GetLayoutVersion :self (Variables|Default|GetInventoryComponent))))))''')
 context=unreal.load_asset(R+'Interaction/IMC_SurvivorInteraction')
 for slot,keyname,name in [(0,'One','Primary'),(1,'Two','Secondary'),(2,'Three','Sidearm')]:
  n='IA_Select'+name
  action=unreal.load_asset(R+'Interaction/'+n)
  if not action:
   f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',unreal.InputAction)
   action=unreal.AssetToolsHelpers.get_asset_tools().create_asset(n,R+'Interaction',unreal.InputAction,f)
  action.set_editor_property('value_type',unreal.InputActionValueType.BOOLEAN)
  context.unmap_all_keys_from_action(action);key=unreal.Key();key.import_text(keyname);context.map_key(action,key)
  unreal.EditorAssetLibrary.save_loaded_asset(action,only_if_is_dirty=False)
  fname='Select'+name
  B.write_graph_dsl(fn(fname),'(fn '+fname+' () (CallFunction|RequestSelectWeapon :Slot '+str(slot)+'))')
  B.compile_blueprint(pc);_BlueprintCache.invalidate(pc)
  if not any(isinstance(x,unreal.K2Node_EnhancedInputAction) and n in B._get_node_info(x).type_id for x in B.find_nodes(g)):
   e=B.create_node(g,'Input|EnhancedActionEvents|'+n,unreal.IntPoint(0,3000+slot*300))
   c=B.create_node(g,'CallFunction|'+fname,unreal.IntPoint(400,3000+slot*300))
   B.connect_pins(pin(e,'Started',True),pin(c,'execute'))
 # A newly possessed pawn starts holstered and receives its equipment display.
 B.write_graph_dsl(g,'''(event EventOnPossess (PossessedPawn)
  (Class|BPInventoryComponent|SetActiveWeaponInstance :self (Variables|Default|GetInventoryComponent) :ActiveWeaponInstance "")
  (Class|BPInventoryComponent|SyncWeaponPresentation :self (Variables|Default|GetInventoryComponent)))''')
 B.compile_blueprint(pc,warnings_as_errors=True)
 assert pc.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE
 for obj in [pc,context]:assert unreal.EditorAssetLibrary.save_loaded_asset(obj,only_if_is_dirty=False)
 print('WEAPON_INPUT_COMPLETE')

