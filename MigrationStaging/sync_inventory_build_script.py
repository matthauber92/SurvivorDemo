from pathlib import Path
p=Path('MigrationStaging/build_inventory_ui_logic.py');s=p.read_text()
for kind,pin in [('Move','bNewMoveInput'),('Look','bNewLookInput')]:
 for v in ['true','false']:s=s.replace('Input|SetIgnore'+kind+'Input '+v,'Input|SetIgnore'+kind+'Input :'+pin+' '+v)
a=s.index("g=B.get_graph(inv,'TryAddItem');old=B.read_graph_dsl(g)")
b=s.index('for b in [ui,pc,inv]:',a)
s=s[:a]+'''# Preserve the original inventory implementation and append a completion notification.
import ast
source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_inventory_logic.py').read_text())
for node in ast.walk(source):
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='write' and ast.literal_eval(node.args[0])=='TryAddItem':
  code=ast.literal_eval(node.args[1]).replace('(return true)','(CallFunction|NotifyInventoryChanged) (return true)')
  B.write_graph_dsl(B.get_graph(inv,'TryAddItem'),code)
''' + s[b:]
p.write_text(s)
