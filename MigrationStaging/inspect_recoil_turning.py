import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.object import ObjectTools as O
report={}
char=unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter')
for path in ['/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter','/Game/Blueprints/SandboxCharacter_CMC_ABP']:
 bp=unreal.load_asset(path);report[path]={}
 for g in B.list_graphs(bp):
  if any(s.lower() in g.get_name().lower() for s in ['rotation','turn','root','hipfire','shot','ShoulderCamera']):report[path][g.get_name()]=B.read_graph_dsl(g)
 print('VARS',path,[str(n) for n in B.list_variables(bp) if any(s in str(n).lower() for s in ['yaw','root','rotate','turn'])])
for path in ['/Game/AIExample/Combat/Animation/Survivor_MM_Rifle_Fire','/Game/AIExample/Combat/Animation/Survivor_MF_Rifle_Idle_ADS','/Game/Characters/Mannequins/Anims/Rifle/MM_Rifle_Fire']:
 a=unreal.load_asset(path);print('ANIMATION',path)
 for n in ['additive_anim_type','base_pose_type','ref_pose_seq','enable_root_motion','force_root_lock','sequence_length','ref_frame_index']:
  try:print(n,a.get_editor_property(n))
  except Exception as e:print(n,str(e))
(Path(unreal.Paths.project_saved_dir())/'recoil-turn-inspect.json').write_text(json.dumps(report,indent=2))
