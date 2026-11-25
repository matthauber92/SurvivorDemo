import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
result={}
for name in ['Items/BP_InventoryComponent','Items/BP_InventoryPlayerController','UI/WBP_Inventory']:
 bp=unreal.load_asset('/Game/AIExample/'+name)
 result[name]={g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(bp)}
(Path(unreal.Paths.project_saved_dir())/'EquipmentValidation/current-graphs.json').write_text(json.dumps(result,indent=2))
print(result['Items/BP_InventoryComponent']['TryAddItem'])
