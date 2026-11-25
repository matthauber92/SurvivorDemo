import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
bp=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP');g=B.get_graph(bp,'ShouldTurnInPlace')
comparison=next(n for n in B.find_nodes(g) if B._get_node_info(n).type_id=='Math|Float|float>=float')
B.set_pin_value(pin(comparison,'B'),'35.0')
original_or=next(n for n in B.find_nodes(g) if B._get_node_info(n).type_id=='Math|Boolean|ORBoolean')
oldout=next(p for p in B._get_node_info(original_or).output_pins if p.name=='ReturnValue');destination=oldout.connected_pins[0]
weight=B.create_node(g,'Variables|Default|GetPistolLayerWeight',unreal.IntPoint(0,700))
armed=B.create_node(g,'Utilities|Operators|Greater(>)',unreal.IntPoint(200,700));B.connect_pins(pin(weight,'PistolLayerWeight',True),pin(armed,'A'));B.set_pin_value(pin(armed,'B'),'0.1')
combined=B.create_node(g,'Math|Boolean|ORBoolean',unreal.IntPoint(500,700));B.connect_pins(pin(armed,'ReturnValue',True),pin(combined,'A'))
B.break_pins(oldout.pin_id,destination);B.connect_pins(oldout.pin_id,pin(combined,'B'));B.connect_pins(pin(combined,'ReturnValue',True),destination)
save(bp)
print('TURN_IN_PLACE_TRIGGERS_BEFORE_45_DEGREE_LIMIT')

