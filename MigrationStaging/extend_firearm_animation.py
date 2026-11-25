import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from weapon_extension_helpers import *
from editor_toolset.toolsets.blueprint import _BlueprintCache
bp=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP');var(bp,'UseShotgunPose','bool');B.compile_blueprint(bp,warnings_as_errors=True);_BlueprintCache.invalidate(bp)
code=code_from('fix_pistol_movement.py','UpdatePistolLayer')
code=code.replace('(and (== (Class|BPSurvivorInteractionCharacter|GetPublicActiveSlot :self Pawn) 2) (== (Class|BPSurvivorInteractionCharacter|GetPublicSidearm :self Pawn) "Weapon.Pistol"))',supported('(Class|BPSurvivorInteractionCharacter|GetActiveFirearmID :self Pawn)'))
code=code.replace(' (bind Moving',' (Variables|Default|SetUseShotgunPose (== (Class|BPSurvivorInteractionCharacter|GetActiveFirearmID :self Pawn) "Weapon.Shotgun"))\n (bind Moving')
write(bp,'UpdatePistolLayer',code)
g=B.get_graph(bp,'AnimGraph')
if not any('Survivor_AO_Rifle' in B._get_node_info(n).type_id for n in B.find_nodes(g)):
 slot=next(n for n in B.find_nodes(g) if isinstance(n,unreal.AnimGraphNode_Slot) and str(n.get_editor_property('node').get_editor_property('slot_name'))=='PistolUpperBody')
 old=next(p for p in B._get_node_info(slot).input_pins if p.name=='Source').connected_pins[0]
 print('BLENDTYPES',B.find_node_types(g,'Blend Poses by bool',[]))
 seq=B.create_node(g,"Animation|Sequences|Play'Survivor_MF_Rifle_Idle_ADS'",unreal.IntPoint(1800,1000))
 ao=B.create_node(g,"Animation|BlendSpaces|AimOffsetPlayer'Survivor_AO_Rifle'",unreal.IntPoint(2100,1000))
 blend=B.create_node(g,'Animation|Blends|BlendPosesbybool',unreal.IntPoint(2400,650))
 getter=B.create_node(g,'Variables|Default|GetUseShotgunPose',unreal.IntPoint(2200,1200))
 pitch=B.create_node(g,'Variables|Default|GetPistolAimPitch',unreal.IntPoint(1800,1300))
 B.connect_pins(pin(seq,'Pose',True),pin(ao,'BasePose'));B.connect_pins(pin(pitch,'PistolAimPitch',True),pin(ao,'Y'))
 B.break_pins(old,pin(slot,'Source'));B.connect_pins(old,pin(blend,'BlendPose_1'));B.connect_pins(pin(ao,'Pose',True),pin(blend,'BlendPose_0'));B.connect_pins(pin(getter,'UseShotgunPose',True),pin(blend,'bActiveValue'));B.connect_pins(pin(blend,'Pose',True),pin(slot,'Source'))
save(bp)
