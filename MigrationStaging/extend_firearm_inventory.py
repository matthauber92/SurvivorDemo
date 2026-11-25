import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from weapon_extension_helpers import *
from editor_toolset.toolsets.blueprint import _BlueprintCache
bp=asset('Items/BP_InventoryComponent')
fn(bp,'GetActiveWeaponID',[],[('ID','name')])
write(bp,'GetActiveWeaponID','''(fn GetActiveWeaponID ()
 (bind Index (CallFunction|GetWeaponIndex :Instance (Variables|Default|GetActiveWeaponInstance)))
 (if (>= Index 0) (return (Utilities|Array|Get(acopy) (Variables|Default|GetWeaponItemIDs) Index))) (return "None"))''')
for name,typ,rev,shot,default in [('GetActiveAmmoID','name','"Ammo.Revolver"','"Ammo.Shotgun"','"Ammo.Handgun"'),('GetActiveCapacity','int','6','2','15'),('GetActiveFireDelay','float','0.45','0.8','0.22'),('GetActiveReloadDuration','float','2.8','3.0','2.0')]:
 fn(bp,name,[],[('Value',typ)])
 write(bp,name,f'''(fn {name} () (bind ID (CallFunction|GetActiveWeaponID)) (if (== ID "Weapon.Revolver") (return {rev})) (if (== ID "Weapon.Shotgun") (return {shot})) (return {default}))''')
B.compile_blueprint(bp,warnings_as_errors=True);_BlueprintCache.invalidate(bp)
code=code_from('build_pistol_inventory.py','GetActivePistolIndex')
code=code.replace('(Utilities|String|NotEqualExactly(String) (Variables|Default|GetActiveWeaponInstance) (Utilities|Array|Get(acopy) (Variables|Default|GetEquipmentInstances) 2))','(not (Utilities|Array|ContainsItem (Variables|Default|GetEquipmentInstances) (Variables|Default|GetActiveWeaponInstance)))')
code=code.replace('(== (Utilities|Array|Get(acopy) (Variables|Default|GetWeaponItemIDs) Index) "Weapon.Pistol")',supported('(Utilities|Array|Get(acopy) (Variables|Default|GetWeaponItemIDs) Index)'))
write(bp,'GetActivePistolIndex',code)
code=code_from('build_pistol_inventory.py','ConsumeHandgunAmmo').replace('"Ammo.Handgun"','(CallFunction|GetActiveAmmoID)');write(bp,'ConsumeHandgunAmmo',code)
code=code_from('build_pistol_inventory.py','TickPistolCombat').replace('"Ammo.Handgun"','(CallFunction|GetActiveAmmoID)').replace('(- 15 ','(- (CallFunction|GetActiveCapacity) ')
code=code.replace('(bind Amount (Math|Integer|Min(Integer)','(Variables|Default|SetReloadTransferAmount (Math|Integer|Min(Integer)').replace('(if (> Amount 0)','(if (> (Variables|Default|GetReloadTransferAmount) 0)').replace(' Index) Amount))',' Index) (Variables|Default|GetReloadTransferAmount)))').replace(':Amount Amount)',':Amount (Variables|Default|GetReloadTransferAmount))')
write(bp,'TickPistolCombat',code)
code=code_from('build_pistol_inventory.py','TryPistolAction')
code=code.replace('Index) 15)','Index) (CallFunction|GetActiveCapacity))').replace('"Ammo.Handgun"','(CallFunction|GetActiveAmmoID)').replace('Seconds) 2.0)','Seconds) (CallFunction|GetActiveReloadDuration))').replace('Seconds) 0.22)','Seconds) (CallFunction|GetActiveFireDelay))')
code=code.replace('  (Class|BPSurvivorInteractionCharacter|SetPublicAiming :self Pawn :PublicAiming false)\n  (Class|BPSurvivorInteractionCharacter|SetPublicReloading','  (Class|BPSurvivorInteractionCharacter|SetPublicReloading')
code=code.replace('500.0','850.0').replace('(Variables|Default|SetNextFireTime (+','''(if (< (Math|Vector|DotProduct (Math|Vector|Normalize ViewDirection) (Math|Vector|GetForwardVector (Pawn|GetControlRotation :self (Pawn|GetController :self Pawn)))) 0.5) (return false))
 (Variables|Default|SetNextFireTime (+''')
write(bp,'TryPistolAction',code);save(bp)
print('THREE_FIREARM_INVENTORY_READY')
