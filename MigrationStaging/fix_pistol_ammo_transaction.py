import unreal,sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
bp=asset('Items/BP_InventoryComponent')
with toolset_registry.tool_raising_exceptions():
 var(bp,'ReloadTransferAmount','int')
 source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_pistol_inventory.py').read_text())
 code=next(ast.literal_eval(n.args[2]) for n in ast.walk(source) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='write' and n.args[1].value=='TickPistolCombat')
 code=code.replace('(bind Amount (Math|Integer|Min(Integer)', '(Variables|Default|SetReloadTransferAmount (Math|Integer|Min(Integer)')
 code=code.replace('(if (> Amount 0)','(if (> (Variables|Default|GetReloadTransferAmount) 0)').replace(' Index) Amount))',' Index) (Variables|Default|GetReloadTransferAmount)))').replace(':Amount Amount)',':Amount (Variables|Default|GetReloadTransferAmount))')
 write(bp,'TickPistolCombat',code);save(bp)
