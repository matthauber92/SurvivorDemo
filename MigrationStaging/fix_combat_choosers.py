import unreal,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
old='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/'
new='/Game/AIExample/Combat/Animation/'
mapping={}
for suffix in ['', '_Dense','_Sparse','_ExtremeSparse']:
 name='CHT_PoseSearchDatabases'+suffix
 src=old+name;dst=new+name
 c=unreal.load_asset(dst) or unreal.EditorAssetLibrary.duplicate_asset(src,dst);mapping[src+'.'+name]=dst+'.'+name
for src,dst in mapping.items():
 c=unreal.load_asset(dst)
 contexts=c.get_editor_property('context_data')
 for ctx in contexts:ctx.import_text(ctx.export_text().replace('/Game/Blueprints/SandboxCharacter_CMC_ABP.SandboxCharacter_CMC_ABP_C','/Game/AIExample/Combat/Animation/ABP_SurvivorCombat.ABP_SurvivorCombat_C'))
 c.set_editor_property('context_data',contexts)
 results=c.get_editor_property('results_structs')
 for r in results:
  txt=r.export_text()
  for a,b in mapping.items():txt=txt.replace(a,b)
  r.import_text(txt)
 c.set_editor_property('results_structs',results)
 unreal.EditorAssetLibrary.save_loaded_asset(c,only_if_is_dirty=False)
bp=asset('Combat/Animation/ABP_SurvivorCombat')
for g in B.list_graphs(bp):
 for n in B.find_nodes(g):
  info=B._get_node_info(n)
  if 'Chooser' in info.type_id:
   print('CHOOSER_NODE',g.get_name(),n.get_name(),info)
   print('NODE_PROPERTIES',unreal.ToolsetLibrary.get_object_properties(n,[]))
