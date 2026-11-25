import unreal,json,ast
import toolset_registry
import sys
sys.path.insert(0,str(__import__('pathlib').Path(unreal.Paths.project_dir())/'MigrationStaging'))
import equipment_dsl,importlib
importlib.reload(equipment_dsl)
from equipment_dsl import typed
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B,ContainerType,_BlueprintCache
R='/Game/AIExample/';out=Path(unreal.Paths.project_saved_dir())/'EquipmentValidation'
inv=unreal.load_asset(R+'Items/BP_InventoryComponent');definition=unreal.load_asset(R+'Items/PDA_ItemDefinition')
def var(bp,n,t,array=False):
 if n not in B.list_variables(bp):
  B.add_variable(bp,n,t,container_type=ContainerType.ARRAY if array else None)
def fn(bp,n,ins=[],outs=[],locals=[]):
 g=B.get_graph(bp,n)
 if not g:
  g=B.add_function_graph(bp,n)
  for k,t in ins:B.add_function_param(g,k,t,True)
  for k,t in outs:B.add_function_param(g,k,t,False)
  for k,t in locals:B.add_variable(bp,k,t,graph=g)
 return g
def write(bp,n,s):
 with toolset_registry.tool_raising_exceptions():
  B.write_graph_dsl(B.get_graph(bp,n),typed(s))
 B.compile_blueprint(bp)
 assert bp.get_editor_property('status') in [unreal.BlueprintStatus.BS_UP_TO_DATE,unreal.BlueprintStatus.BS_UP_TO_DATE_WITH_WARNINGS],(n,bp.get_editor_property('status'))
 print('EQUIPMENT_GRAPH',n)
for n,t in [('EquipmentType','name'),('InitialMagazine','int')]:
 var(definition,n,t);B.set_variable_instance_editable(definition,n,True)
B.compile_blueprint(definition);unreal.EditorAssetLibrary.save_loaded_asset(definition)
for n,t in [('BackpackInstances','string'),('EquipmentInstances','string'),('WeaponInstances','string'),('WeaponItemIDs','name'),('WeaponTypes','name'),('WeaponMagazines','int')]:
 var(inv,n,t,True);B.set_variable_replication(inv,n,unreal.BlueprintVariableReplication.REP_NOTIFY)
var(inv,'EquipmentResult','string');B.set_variable_replication(inv,'EquipmentResult',unreal.BlueprintVariableReplication.REP_NOTIFY)
B.compile_blueprint(inv)
unreal.get_default_object(inv.generated_class()).set_editor_property('EquipmentInstances',['','',''])
for n in ['BackpackInstances','EquipmentInstances','WeaponInstances','WeaponItemIDs','WeaponTypes','WeaponMagazines','EquipmentResult']:
 write(inv,'OnRep_'+n,'(fn OnRep_'+n+' () (CallFunction|NotifyInventoryChanged))')
fn(inv,'GetWeaponIndex',[('Instance','string')],[('Index','int')])
write(inv,'GetWeaponIndex','''(fn GetWeaponIndex (Instance)
 (if (!= Instance "") (return (Utilities|Array|FindItem (Variables|Default|GetWeaponInstances) Instance)))
 (return -1))''')
fn(inv,'GetInstanceAtLocation',[('Location','int')],[('Instance','string')])
write(inv,'GetInstanceAtLocation','''(fn GetInstanceAtLocation (Location)
 (if (and (>= Location 0) (< Location 8))
  (bind Index (Utilities|Array|Get(acopy) (Variables|Default|GetSlotOrder) Location))
  (if (Utilities|Array|IsValidIndex (Variables|Default|GetBackpackInstances) Index)
   (return (Utilities|Array|Get(acopy) (Variables|Default|GetBackpackInstances) Index))))
 (if (and (>= Location 8) (< Location 11))
  (return (Utilities|Array|Get(acopy) (Variables|Default|GetEquipmentInstances) (- Location 8))))
 (return ""))''')
fn(inv,'CanEquipInstance',[('Instance','string'),('EquipmentSlot','int')],[('Compatible','bool')])
write(inv,'CanEquipInstance','''(fn CanEquipInstance (Instance EquipmentSlot)
 (bind Index (CallFunction|GetWeaponIndex Instance))
 (if (and (>= Index 0) (and (>= EquipmentSlot 0) (< EquipmentSlot 3)))
  (bind Kind (Utilities|Array|Get(acopy) (Variables|Default|GetWeaponTypes) Index))
  (if (== EquipmentSlot 2) (return (== Kind "Sidearm")) (else (return (== Kind "LongGun")))))
 (return false))''')
g=fn(inv,'RegisterWeapon',[],[('Instance','string')],[('CreatedInstance','string')])
if not any(p.name=='Definition' for p in B._get_node_info(next(n for n in B.find_nodes(g) if isinstance(n,unreal.K2Node_FunctionEntry))).output_pins):
 B.add_object_function_param(g,'Definition',definition.generated_class(),True)
write(inv,'RegisterWeapon','''(fn RegisterWeapon (Definition)
 (if (== (Class|PDAItemDefinition|GetCategory Definition) "Weapon")
  (Variables|Default|SetCreatedInstance (Guid|ToString(Guid) (Guid|NewGuid)))
  (Utilities|Array|Add (Variables|Default|GetWeaponInstances) (Variables|Default|GetCreatedInstance))
  (Utilities|Array|Add (Variables|Default|GetWeaponItemIDs) (Class|PDAItemDefinition|GetItemID Definition))
  (Utilities|Array|Add (Variables|Default|GetWeaponTypes) (Class|PDAItemDefinition|GetEquipmentType Definition))
  (Utilities|Array|Add (Variables|Default|GetWeaponMagazines) (Math|Integer|Max(Integer) 0 (Class|PDAItemDefinition|GetInitialMagazine Definition)))
  (return (Variables|Default|GetCreatedInstance)))
 (return ""))''')
fn(inv,'RemoveBackpackEntry',[('Index','int')])
write(inv,'RemoveBackpackEntry','''(fn RemoveBackpackEntry (Index)
 (Utilities|Array|RemoveIndex (Variables|Default|GetItemIDs) Index)
 (Utilities|Array|RemoveIndex (Variables|Default|GetQuantities) Index)
 (Utilities|Array|RemoveIndex (Variables|Default|GetBackpackInstances) Index)
 (for i (range 8)
  (bind Value (Utilities|Array|Get(acopy) (Variables|Default|GetSlotOrder) i))
  (if (== Value Index) (Utilities|Array|SetArrayElem (Variables|Default|GetSlotOrder) i 7)
   (else (if (> Value Index) (Utilities|Array|SetArrayElem (Variables|Default|GetSlotOrder) i (- Value 1)))))))''')
fn(inv,'RejectEquipment',[('Message','string')],[('Moved','bool')])
write(inv,'RejectEquipment','''(fn RejectEquipment (Message)
 (Variables|Default|SetEquipmentResult Message)
 (CallFunction|NotifyInventoryChanged)
 (return false))''')
args=[('SourceLocation','int'),('TargetLocation','int'),('ExpectedInstance','string'),('ExpectedVersion','int')]
fn(inv,'TryTransferWeapon',args,[('Moved','bool')],[('SourceInstance','string'),('TargetInstance','string'),('SourceRecord','int'),('TargetRecord','int'),('StorageIndex','int'),('NewIndex','int')])
write(inv,'TryTransferWeapon','''(fn TryTransferWeapon (SourceLocation TargetLocation ExpectedInstance ExpectedVersion)
 (if (not (Networking|HasAuthority (Components|GetOwner))) (return false))
 (if (or (or (< SourceLocation 0) (>= SourceLocation 11)) (or (< TargetLocation -1) (>= TargetLocation 11)))
  (return (CallFunction|RejectEquipment "Invalid equipment request.")))
 (if (or (== SourceLocation TargetLocation) (!= ExpectedVersion (Variables|Default|GetLayoutVersion)))
  (return (CallFunction|RejectEquipment "Inventory changed. Select the weapon again.")))
 (Variables|Default|SetSourceInstance (CallFunction|GetInstanceAtLocation SourceLocation))
 (if (or (== ExpectedInstance "") (!= ExpectedInstance (Variables|Default|GetSourceInstance)))
  (return (CallFunction|RejectEquipment "Select a weapon first.")))
 (Variables|Default|SetSourceRecord (CallFunction|GetWeaponIndex (Variables|Default|GetSourceInstance)))
 (if (< (Variables|Default|GetSourceRecord) 0) (return (CallFunction|RejectEquipment "Invalid weapon instance.")))
 (Variables|Default|SetTargetInstance (CallFunction|GetInstanceAtLocation TargetLocation))
 (Variables|Default|SetTargetRecord (CallFunction|GetWeaponIndex (Variables|Default|GetTargetInstance)))
 (if (< SourceLocation 8)
  (if (< TargetLocation 8) (return (CallFunction|RejectEquipment "Use backpack drag to rearrange items.")))
  (if (not (CallFunction|CanEquipInstance (Variables|Default|GetSourceInstance) (- TargetLocation 8)))
   (return (CallFunction|RejectEquipment "Incompatible slot: long guns use Primary or Secondary; pistols use Sidearm.")))
  (Variables|Default|SetStorageIndex (Utilities|Array|Get(acopy) (Variables|Default|GetSlotOrder) SourceLocation))
  (if (== (Variables|Default|GetTargetInstance) "")
   (Utilities|Array|SetArrayElem (Variables|Default|GetEquipmentInstances) (- TargetLocation 8) (Variables|Default|GetSourceInstance))
   (CallFunction|RemoveBackpackEntry (Variables|Default|GetStorageIndex))
   (else
    (if (< (Variables|Default|GetTargetRecord) 0) (return (CallFunction|RejectEquipment "Invalid target weapon.")))
    (Utilities|Array|SetArrayElem (Variables|Default|GetItemIDs) (Variables|Default|GetStorageIndex) (Utilities|Array|Get(acopy) (Variables|Default|GetWeaponItemIDs) (Variables|Default|GetTargetRecord)))
    (Utilities|Array|SetArrayElem (Variables|Default|GetBackpackInstances) (Variables|Default|GetStorageIndex) (Variables|Default|GetTargetInstance))
    (Utilities|Array|SetArrayElem (Variables|Default|GetEquipmentInstances) (- TargetLocation 8) (Variables|Default|GetSourceInstance))))
  (else
   (if (>= TargetLocation 8)
    (if (not (CallFunction|CanEquipInstance (Variables|Default|GetSourceInstance) (- TargetLocation 8)))
     (return (CallFunction|RejectEquipment "Weapon is incompatible with that equipment slot.")))
    (if (!= (Variables|Default|GetTargetInstance) "")
     (if (not (CallFunction|CanEquipInstance (Variables|Default|GetTargetInstance) (- SourceLocation 8)))
      (return (CallFunction|RejectEquipment "The other weapon cannot use the source equipment slot."))))
    (Utilities|Array|SetArrayElem (Variables|Default|GetEquipmentInstances) (- TargetLocation 8) (Variables|Default|GetSourceInstance))
    (Utilities|Array|SetArrayElem (Variables|Default|GetEquipmentInstances) (- SourceLocation 8) (Variables|Default|GetTargetInstance))
    (else
     (Variables|Default|SetStorageIndex -1)
     (if (>= TargetLocation 0) (Variables|Default|SetStorageIndex (Utilities|Array|Get(acopy) (Variables|Default|GetSlotOrder) TargetLocation)))
     (if (Utilities|Array|IsValidIndex (Variables|Default|GetItemIDs) (Variables|Default|GetStorageIndex))
      (if (not (CallFunction|CanEquipInstance (Variables|Default|GetTargetInstance) (- SourceLocation 8)))
       (return (CallFunction|RejectEquipment "Cannot swap equipment with that backpack item.")))
      (Utilities|Array|SetArrayElem (Variables|Default|GetItemIDs) (Variables|Default|GetStorageIndex) (Utilities|Array|Get(acopy) (Variables|Default|GetWeaponItemIDs) (Variables|Default|GetSourceRecord)))
      (Utilities|Array|SetArrayElem (Variables|Default|GetBackpackInstances) (Variables|Default|GetStorageIndex) (Variables|Default|GetSourceInstance))
      (Utilities|Array|SetArrayElem (Variables|Default|GetEquipmentInstances) (- SourceLocation 8) (Variables|Default|GetTargetInstance))
      (else
       (if (>= (Utilities|Array|Length (Variables|Default|GetItemIDs)) 8)
        (return (CallFunction|RejectEquipment "Backpack full. Free a slot before unequipping.")))
       (Variables|Default|SetNewIndex (Utilities|Array|Length (Variables|Default|GetItemIDs)))
       (Utilities|Array|Add (Variables|Default|GetItemIDs) (Utilities|Array|Get(acopy) (Variables|Default|GetWeaponItemIDs) (Variables|Default|GetSourceRecord)))
       (Utilities|Array|Add (Variables|Default|GetQuantities) 1)
       (Utilities|Array|Add (Variables|Default|GetBackpackInstances) (Variables|Default|GetSourceInstance))
       (Utilities|Array|SetArrayElem (Variables|Default|GetEquipmentInstances) (- SourceLocation 8) "")
       (if (>= TargetLocation 0)
        (Utilities|Array|SwapArrayElements (Variables|Default|GetSlotOrder) TargetLocation (Utilities|Array|FindItem (Variables|Default|GetSlotOrder) (Variables|Default|GetNewIndex))))))))))
 (Variables|Default|SetLayoutVersion (+ (Variables|Default|GetLayoutVersion) 1))
 (Variables|Default|SetEquipmentResult "Equipment updated.")
 (CallFunction|NotifyInventoryChanged)
 (return true))''')
# Extend the existing pickup storage; do not replace its stack/capacity behavior.
source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_inventory_logic.py').read_text())
for node in ast.walk(source):
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='write':
  n=ast.literal_eval(node.args[0]);code=ast.literal_eval(node.args[1])
  if n=='CanAddItem':
   code=code.replace('(:"Is Valid"','''(:"Is Valid"
   (if (== (Class|PDAItemDefinition|GetCategory Definition) "Weapon")
    (if (or (!= (Class|PDAItemDefinition|GetMaxStackSize Definition) 1) (not (or (== (Class|PDAItemDefinition|GetEquipmentType Definition) "LongGun") (== (Class|PDAItemDefinition|GetEquipmentType Definition) "Sidearm")))) (return false)))''',1)
   write(inv,n,code)
  if n=='TryAddItem':
   code=code.replace('(Utilities|Array|Add (Variables|Default|GetQuantities) (Variables|Default|GetTransfer))','''(Utilities|Array|Add (Variables|Default|GetQuantities) (Variables|Default|GetTransfer))
    (Utilities|Array|Add (Variables|Default|GetBackpackInstances) (CallFunction|RegisterWeapon Definition))''')
   code=code.replace('(return true)','''(Variables|Default|SetLayoutVersion (+ (Variables|Default|GetLayoutVersion) 1))
   (CallFunction|NotifyInventoryChanged) (return true)''')
   write(inv,n,code)
B.compile_blueprint(inv,warnings_as_errors=True)
assert inv.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE
unreal.EditorAssetLibrary.save_loaded_asset(inv,only_if_is_dirty=False)
# Definitions only: no attachment, combat, or animation behavior.
at=unreal.AssetToolsHelpers.get_asset_tools()
for name,id,title,kind,mesh,icon in [
 ('DA_PistolItem','Weapon.Pistol','Pistol','Sidearm',R+'Weapons/TheHouse/04_Weapons/Pistol/Mesh/SM_Pistol',R+'Weapons/TheHouse/04_Weapons/Pistol/Image/IMG_Pistol'),
 ('DA_EquipmentTestLongGun','Weapon.TestLongGun','Long gun (test)','LongGun','/Engine/BasicShapes/Cube','/Engine/EngineResources/WhiteSquareTexture')]:
 path=R+'Items/'+name
 obj=unreal.load_asset(path)
 if not obj:
  f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',definition.generated_class());obj=at.create_asset(name,R+'Items',unreal.DataAsset,f)
 for k,v in {'ItemID':id,'DisplayName':unreal.Text(title),'Category':'Weapon','MaxStackSize':1,'EquipmentType':kind,'InitialMagazine':0,'WorldMesh':unreal.load_asset(mesh),'InventoryIcon':unreal.load_asset(icon),'Description':unreal.Text('Equipment-slot item. Combat is not implemented.')}.items():obj.set_editor_property(k,v)
 unreal.EditorAssetLibrary.save_loaded_asset(obj)
print('EQUIPMENT_FOUNDATION_COMPLETE')
