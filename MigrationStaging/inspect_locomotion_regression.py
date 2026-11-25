import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out=Path(unreal.Paths.project_saved_dir())/'LocomotionRepair';out.mkdir(exist_ok=True)
bp=unreal.load_asset('/Game/AIExample/Combat/Animation/ABP_SurvivorCombat')
print('GRAPHS',[g.get_name() for g in B.list_graphs(bp)])
print('VARIABLES',B.list_variables(bp))
for name in ['EventGraph','Update_MotionMatching','Update_CharacterState','Update_CharacterMovement','BlueprintThreadSafeUpdateAnimation']:
 g=next((g for g in B.list_graphs(bp) if g.get_name()==name),None)
 if g:
  if name=='EventGraph':
   (out/(name+'.txt')).write_text('\n'.join(str(B._get_node_info(n)) for n in B.find_nodes(g)))
  else:(out/(name+'.txt')).write_text(B.read_graph_dsl(g))
ws=unreal.EditorLevelLibrary.get_pie_worlds(False)
if ws:
 p=unreal.GameplayStatics.get_player_pawn(ws[0],0);a=p.get_component_by_class(unreal.SkeletalMeshComponent).get_anim_instance()
 print('PAWN',p.get_velocity(),p.get_actor_location(),'ANIM',a.get_class().get_name())
 vals={}
 for n in B.list_variables(bp):
  try:vals[n]=str(a.get_editor_property(n))
  except Exception:pass
 (out/'runtime.json').write_text(json.dumps(vals,indent=2));print(vals)

