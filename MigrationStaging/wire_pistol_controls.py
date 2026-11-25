import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
from editor_toolset.toolsets.blueprint import _BlueprintCache
bp=asset('Items/BP_InventoryPlayerController');g=B.get_graph(bp,'EventGraph')
with toolset_registry.tool_raising_exceptions():
 event=next(n for n in B.find_nodes(g) if isinstance(n,unreal.K2Node_CustomEvent) and 'ServerPistolAction' in B._get_node_info(n).type_id)
 if not any(p.connected_pins for p in B._get_node_info(event).output_pins):
  call=B.create_node(g,'Class|BPInventoryComponent|TryPistolAction',unreal.IntPoint(600,4500));getter=B.create_node(g,'Variables|Default|GetInventoryComponent',unreal.IntPoint(300,4800))
  B.connect_pins(pin(event,'then',True),pin(call,'execute'));B.connect_pins(B._get_node_info(getter).output_pins[0].pin_id,pin(call,'self'))
  for n in ['Action','ExpectedInstance','ViewOrigin','ViewDirection']:B.connect_pins(pin(event,n,True),pin(call,n))
 B.compile_blueprint(bp);_BlueprintCache.invalidate(bp)
 fn(bp,'RequestPistolAction',[('Action','int')])
 write(bp,'RequestPistolAction','''(fn RequestPistolAction (Action)
 (if (Pawn|IsLocalController)
  (if (or (== Action 0) (not (Variables|Default|GetInventoryOpen)))
   (bind Camera (Variables|PlayerController|GetPlayerCameraManager))
   (CallFunction|ServerPistolAction :Action Action :ExpectedInstance (Class|BPInventoryComponent|GetActiveWeaponInstance :self (Variables|Default|GetInventoryComponent)) :ViewOrigin (Camera|GetCameraLocation :self Camera) :ViewDirection (Math|Vector|GetForwardVector (Camera|GetCameraRotation :self Camera))))))''')
 for name,action in [('PistolAimStart',1),('PistolAimStop',0),('PistolFire',2),('PistolReload',3)]:
  fn(bp,name);write(bp,name,'(fn '+name+' () (CallFunction|RequestPistolAction :Action '+str(action)+'))')
 B.compile_blueprint(bp);_BlueprintCache.invalidate(bp)
 context=asset('Interaction/IMC_SurvivorInteraction')
 for name,keyname,func in [('IA_PistolAim','RightMouseButton','PistolAimStart'),('IA_PistolFire','LeftMouseButton','PistolFire'),('IA_PistolReload','R','PistolReload')]:
  action=asset('Combat/'+name)
  if not action:
   factory=unreal.DataAssetFactory();factory.set_editor_property('data_asset_class',unreal.InputAction);action=unreal.AssetToolsHelpers.get_asset_tools().create_asset(name,R+'Combat',unreal.InputAction,factory)
  action.set_editor_property('value_type',unreal.InputActionValueType.BOOLEAN)
  action.set_editor_property('consume_input',False if name=='IA_PistolAim' else True)
  context.unmap_all_keys_from_action(action);key=unreal.Key();key.import_text(keyname);context.map_key(action,key)
  unreal.EditorAssetLibrary.save_loaded_asset(action,only_if_is_dirty=False)
  if not any(isinstance(n,unreal.K2Node_EnhancedInputAction) and name in B._get_node_info(n).type_id for n in B.find_nodes(g)):
   e=B.create_node(g,'Input|EnhancedActionEvents|'+name,unreal.IntPoint(0,5200));c=B.create_node(g,'CallFunction|'+func,unreal.IntPoint(400,5200));B.connect_pins(pin(e,'Started',True),pin(c,'execute'))
   if name=='IA_PistolAim':
    for output in ['Completed','Canceled']:
     c=B.create_node(g,'CallFunction|PistolAimStop',unreal.IntPoint(400,5500));B.connect_pins(pin(e,output,True),pin(c,'execute'))
 B.write_graph_dsl(g,'''(event EventTick (DeltaSeconds)
 (Class|BPInventoryComponent|TickPistolCombat :self (Variables|Default|GetInventoryComponent)))''')
 save(bp);unreal.EditorAssetLibrary.save_loaded_asset(context,only_if_is_dirty=False)
 print('PISTOL_CONTROLS_READY')


