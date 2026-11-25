import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out={}
for rel in ['Items/BP_InventoryComponent','Items/BP_InventoryPlayerController','Items/PDA_ItemDefinition','UI/WBP_Inventory','Items/BP_ItemPickup']:
 bp=unreal.load_asset('/Game/AIExample/'+rel);out[rel]={'graphs':[g.get_name() for g in B.list_graphs(bp)],'variables':list(B.list_variables(bp))}
 for name in out[rel]['graphs']:
  if any(x in name for x in ['Definition','Pistol','Sync','Register','Display','ItemName','Label']):out[rel][name]=B.read_graph_dsl(B.get_graph(bp,name))
Path(unreal.Paths.project_saved_dir(),'weapon-extension-inspect.json').write_text(json.dumps(out,indent=2))
