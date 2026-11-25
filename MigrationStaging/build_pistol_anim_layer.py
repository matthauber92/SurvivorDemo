import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
path=R+'Combat/Animation/ABP_SurvivorCombat'
bp=unreal.load_asset(path) or unreal.EditorAssetLibrary.duplicate_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP',path)
g=B.get_graph(bp,'AnimGraph')
with toolset_registry.tool_raising_exceptions():
 var(bp,'PistolLayerWeight','float');var(bp,'PistolAimPitch','float')
 fn(bp,'UpdatePistolLayer',[('DeltaSeconds','float')])
 write(bp,'UpdatePistolLayer','''(fn UpdatePistolLayer (DeltaSeconds)
 (bind Pawn (Utilities|Casting|CastToBP_SurvivorInteractionCharacter (Animation|TryGetPawnOwner)))
 (Variables|Default|SetPistolLayerWeight (Math|Interpolation|FInterpTo (Variables|Default|GetPistolLayerWeight) (select (and (== (Class|BPSurvivorInteractionCharacter|GetPublicActiveSlot :self Pawn) 2) (== (Class|BPSurvivorInteractionCharacter|GetPublicSidearm :self Pawn) "Weapon.Pistol")) 1.0 0.0) DeltaSeconds 10.0))
 (bind (Roll Pitch Yaw) (Math|Rotator|BreakRotator (Pawn|GetBaseAimRotation :self Pawn)))
 (Variables|Default|SetPistolAimPitch (Math|Float|Clamp(Float) (Math|Rotator|NormalizeAxis Pitch) -70.0 70.0)))''')
 B.compile_blueprint(bp)
 eg=B.get_graph(bp,'EventGraph')
 if not any('UpdatePistolLayer' in B._get_node_info(n).type_id for n in B.find_nodes(eg)):
  event=next(n for n in B.find_nodes(eg) if 'EventBlueprintUpdateAnimation' in B._get_node_info(n).type_id)
  e=pin(event,'then',True);old=list(next(p for p in B._get_node_info(event).output_pins if p.name=='then').connected_pins)
  call=B.create_node(eg,'CallFunction|UpdatePistolLayer',unreal.IntPoint(350,-400))
  for dst in old:B.break_pins(e,dst);B.connect_pins(pin(call,'then',True),dst)
  B.connect_pins(e,pin(call,'execute'));B.connect_pins(pin(event,'DeltaTimeX',True),pin(call,'DeltaSeconds'))
 nodes=list(B.find_nodes(g))
 if not any(n.get_name().startswith('PistolLayer') for n in nodes):
  root=next(n for n in nodes if isinstance(n,unreal.AnimGraphNode_Root));rootpin=B._get_node_info(root).input_pins[0].pin_id
  old=B._get_node_info(root).input_pins[0].connected_pins[0]
  seq=B.create_node(g,'Animation|Sequences|SequencePlayer',unreal.IntPoint(1800,400))
  data=seq.get_editor_property('node');data.set_editor_property('sequence',asset('Combat/Animation/Survivor_MF_Pistol_Idle_ADS'));seq.set_editor_property('node',data)
  slot=B.create_node(g,"Animation|Montage|Slot'DefaultSlot'",unreal.IntPoint(2200,400))
  data=slot.get_editor_property('node');data.set_editor_property('slot_name','PistolUpperBody');slot.set_editor_property('node',data)
  blend=B.create_node(g,'Animation|Blends|Layeredblendperbone',unreal.IntPoint(2600,0));blend.rename('PistolLayer_Blend')
  data=blend.get_editor_property('node')
  layer=unreal.InputBlendPose();f=unreal.BranchFilter();f.set_editor_property('bone_name','spine_01');f.set_editor_property('blend_depth',3);layer.set_editor_property('branch_filters',[f]);data.set_editor_property('layer_setup',[layer]);data.set_editor_property('mesh_space_rotation_blend',True);blend.set_editor_property('node',data)
  weight=B.create_node(g,'Variables|Default|GetPistolLayerWeight',unreal.IntPoint(2350,650))
  B.break_pins(old,rootpin);B.connect_pins(old,pin(blend,'BasePose'));B.connect_pins(pin(seq,'Pose',True),pin(slot,'Source'));B.connect_pins(pin(slot,'Pose',True),pin(blend,'BlendPoses_0'));B.connect_pins(B._get_node_info(weight).output_pins[0].pin_id,pin(blend,'BlendWeights_0'));B.connect_pins(pin(blend,'Pose',True),rootpin)
 save(bp)
 print('AO_TYPES',[x for x in B.find_node_types(g,'Survivor_AO_Pistol',[])])
 print('PISTOL_ANIM_LAYER_CREATED')

