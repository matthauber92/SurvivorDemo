import unreal,sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
char=asset('Interaction/BP_SurvivorInteractionCharacter')
write(char,'RefreshPistolAim','''(fn RefreshPistolAim ()
 (bind (Sprint Walk Strafe Aim Crouch) (Utilities|Struct|BreakSPlayerInputState (Variables|Input|GetCharacterInputState)))
 (Variables|Input|SetCharacterInputState (Utilities|Struct|MakeSPlayerInputState Sprint Walk Strafe (Variables|Default|GetPublicAiming) Crouch)))''')
save(char)
inv=asset('Items/BP_InventoryComponent')
source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_pistol_inventory.py').read_text())
code=next(ast.literal_eval(n.args[2]) for n in ast.walk(source) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='write' and n.args[1].value=='TryPistolAction')
code=code.replace('  (Class|BPSurvivorInteractionCharacter|SetPublicAiming :self Pawn :PublicAiming false)\n  (Class|BPSurvivorInteractionCharacter|SetPublicReloading','  (Class|BPSurvivorInteractionCharacter|SetPublicReloading')
# Retain a generous cone for networked camera latency while rejecting backwards shots.
code=code.replace('(Variables|Default|SetNextFireTime (+', '''(if (< (Math|Vector|DotProduct (Math|Vector|Normalize ViewDirection) (Math|Vector|GetForwardVector (Pawn|GetControlRotation :self Pawn))) 0.5) (return false))
 (Variables|Default|SetNextFireTime (+''')
write(inv,'TryPistolAction',code);save(inv)
