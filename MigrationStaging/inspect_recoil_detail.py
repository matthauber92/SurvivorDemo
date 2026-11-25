import unreal,json
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.object import ObjectTools as O
for path in ['/Game/AIExample/Combat/Animation/Survivor_MM_Rifle_Fire','/Game/AIExample/Combat/Animation/Survivor_MM_Pistol_Fire']:
 a=unreal.load_asset(path)
 print(path)
 for k in ['additive_anim_type','ref_pose_type','ref_pose_seq','enable_root_motion','force_root_lock','sequence_length']:
  try:print(k,str(a.get_editor_property(k)))
  except:pass
bp=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP')
for g in B.list_graphs(bp):
 for n in B.find_nodes(g):
  if 'OffsetRoot' in n.get_class().get_name():
   print('ROOTNODE',n.get_path_name());print(O.list_properties(n));print(n.get_editor_property("node"))

