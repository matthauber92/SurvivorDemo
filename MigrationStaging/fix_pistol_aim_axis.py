import unreal,sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
bp=asset('Combat/Animation/ABP_SurvivorCombat');g=B.get_graph(bp,'AnimGraph')
with toolset_registry.tool_raising_exceptions():
 ao=next(n for n in B.find_nodes(g) if isinstance(n,unreal.AnimGraphNode_RotationOffsetBlendSpace))
 for pname in ['X','Y']:
  for p in B._get_node_info(ao).input_pins:
   if p.name==pname:
    for src in list(p.connected_pins):B.break_pins(src,p.pin_id)
 getter=next(n for n in B.find_nodes(g) if B._get_node_info(n).type_id.endswith('|GetPistolAimPitch'))
 B.connect_pins(B._get_node_info(getter).output_pins[0].pin_id,pin(ao,'Y'))
 source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_pistol_anim_layer.py').read_text())
 code=next(ast.literal_eval(n.args[2]) for n in ast.walk(source) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='write')
 code=code.replace('(Math|Float|Clamp(Float) (Math|Rotator|NormalizeAxis Pitch) -70.0 70.0)','(/ (Math|Float|Clamp(Float) (Math|Rotator|NormalizeAxis Pitch) -70.0 70.0) 70.0)')
 write(bp,'UpdatePistolLayer',code);save(bp)

