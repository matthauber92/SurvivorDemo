import unreal,json,sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
from editor_toolset.toolsets.object import ObjectTools as O
from editor_toolset.toolsets.blueprint import _BlueprintCache
root=Path(unreal.Paths.project_dir())
paths=json.loads((Path(unreal.Paths.project_saved_dir())/'ShoulderCamera/repaired-animation-contexts.json').read_text())
with toolset_registry.tool_raising_exceptions():
 for path in paths:
  c=unreal.load_asset(path)
  data=json.loads(O.get_properties(c,['ContextData']))
  for v in data['ContextData']:
   if v.get('_structType')=='/Script/Chooser.ContextObjectTypeClass':v['class']['refPath']='/Game/Blueprints/SandboxCharacter_CMC_ABP.SandboxCharacter_CMC_ABP_C'
  assert O.set_properties(c,json.dumps(data))
  assert 'SandboxCharacter_CMC_ABP_C' in c.get_editor_property('context_data')[0].export_text()
  assert unreal.EditorAssetLibrary.save_loaded_asset(c,only_if_is_dirty=False)
 # Keep the sample locomotion Blueprint and its typed chooser tables together.
 source=(root/'MigrationStaging/build_pistol_anim_layer.py').read_text()
 source=source.replace("path=R+'Combat/Animation/ABP_SurvivorCombat'","path='/Game/Blueprints/SandboxCharacter_CMC_ABP'")
 source=source.replace('(Math|Float|Clamp(Float) (Math|Rotator|NormalizeAxis Pitch) -70.0 70.0)','(/ (Math|Float|Clamp(Float) (Math|Rotator|NormalizeAxis Pitch) -85.0 85.0) 90.0)')
 exec(compile(source,'add_pistol_layer_to_locomotion_base','exec'))
 bp=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP');g=B.get_graph(bp,'AnimGraph')
 slot=next(n for n in B.find_nodes(g) if isinstance(n,unreal.AnimGraphNode_Slot) and str(n.get_editor_property('node').get_editor_property('slot_name'))=='PistolUpperBody')
 incoming=next(p for p in B._get_node_info(slot).input_pins if p.name=='Source').connected_pins[0]
 if not isinstance(incoming.node,unreal.AnimGraphNode_RotationOffsetBlendSpace):
  ao=B.create_node(g,"Animation|BlendSpaces|AimOffsetPlayer'Survivor_AO_Pistol'",unreal.IntPoint(2050,400))
  pitch=B.create_node(g,'Variables|Default|GetPistolAimPitch',unreal.IntPoint(1850,650))
  B.break_pins(incoming,pin(slot,'Source'));B.connect_pins(incoming,pin(ao,'BasePose'));B.connect_pins(pin(ao,'Pose',True),pin(slot,'Source'));B.connect_pins(B._get_node_info(pitch).output_pins[0].pin_id,pin(ao,'Y'))
 save(bp)
 char=asset('Interaction/BP_SurvivorInteractionCharacter')
 write(char,'InitializePistolAnimation','''(fn InitializePistolAnimation ()
 (Components|SkeletalMesh|SetAnimInstanceClass :self (Variables|Character|GetMesh) :NewClass "/Game/Blueprints/SandboxCharacter_CMC_ABP.SandboxCharacter_CMC_ABP_C"))''');save(char)
 print('RESTORED_ORIGINAL_LOCOMOTION_WITH_PISTOL_LAYER')
