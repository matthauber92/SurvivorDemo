import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A
out=Path(r'C:\Users\Matt Hauber\Documents\Unreal Projects\AIExample\Saved\ShoulderCamera')
for sub in ['ThirdPerson','SurvivalMan']:
 bp=unreal.load_asset('/Game/'+sub+'/Blueprints/BP_ThirdPersonCharacter')
 report={'variables':str(B.list_variables(bp)),'graphs':[g.get_name() for g in B.list_graphs(bp)]}
 report['components']=str(A.get_components(B.get_default_object(bp)))
 for g in B.list_graphs(bp):
  if any(s in g.get_name().lower() for s in ['camera','zoom','aim','sprint','eventgraph']):
   try:(out/('House-'+sub+'-'+g.get_name().replace('/','_')+'.txt')).write_text(B.read_graph_dsl(g))
   except Exception as e:print(str(e))
   (out/('House-'+sub+'-'+g.get_name().replace('/','_')+'-nodes.txt')).write_text('\n'.join(str(B._get_node_info(n)) for n in B.find_nodes(g)))
 (out/('House-'+sub+'.json')).write_text(json.dumps(report,indent=2))
 print(sub,report)
