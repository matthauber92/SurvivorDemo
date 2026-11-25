import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A
R='/Game/AIExample/';out=Path(unreal.Paths.project_saved_dir())/'WeaponSwitchValidation';out.mkdir(exist_ok=True)
result={}
for name in ['Interaction/BP_SurvivorInteractionCharacter','Items/BP_InventoryPlayerController','Items/BP_InventoryComponent']:
 bp=unreal.load_asset(R+name);cdo=unreal.get_default_object(bp.generated_class())
 result[name]={'graphs':{g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(bp)},'variables':[str(x) for x in B.list_variables(bp)]}
 if 'Character' in name:
  for c in A.get_components(cdo):
   print('COMP',c.get_name(),c.get_class().get_name())
   if isinstance(c,unreal.SkeletalMeshComponent):
    print('SKEL',c.get_editor_property('skeletal_mesh_asset'),c.get_editor_property('hidden_in_game'),c.get_editor_property('relative_transform') if False else c.get_editor_property('relative_location'))
    print('SOCKETS',[str(x) for x in c.get_all_socket_names() if any(t in str(x) for t in ['hand','spine','pelvis','weapon','Weapon'])])
  g=B.get_graph(bp,'EventGraph')
  for term in ['AttachComponent','SetRelative','SetStaticMesh','SetHiddenInGame','GetMesh','GetPawn','GetController','ServerSelect','SetTimer']:
   print('NODES',term,list(B.find_node_types(g,term,[]))[:20])
 print('EVENT',name,result[name]['graphs'].get('EventGraph'))
(out/'before.json').write_text(json.dumps(result,indent=2));print('INSPECTED')
