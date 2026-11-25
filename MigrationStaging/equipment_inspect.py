import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out=Path(unreal.Paths.project_saved_dir())/'EquipmentValidation';out.mkdir(exist_ok=True)
result={}
for path in ['Items/PDA_ItemDefinition','Items/BP_InventoryComponent','Items/BP_InventoryPlayerController','UI/WBP_Inventory']:
 bp=unreal.load_asset('/Game/AIExample/'+path)
 graphs={g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(bp)}
 result[path]={'variables':[str(x) for x in B.list_variables(bp)],'graphs':graphs}
 if path=='UI/WBP_Inventory':
  tree=unreal.find_object(bp,'WidgetTree')
  canvas=unreal.find_object(tree,'InventoryCanvas')
  result[path]['canvas']=[{'index':i,'name':canvas.get_child_at(i).get_name(),'class':canvas.get_child_at(i).get_class().get_name()} for i in range(canvas.get_children_count())]
(out/'before.json').write_text(json.dumps(result,indent=2))
print('EQUIPMENT_INSPECTED',str(out))
