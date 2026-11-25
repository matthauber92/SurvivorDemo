import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
ui=unreal.load_asset('/Game/AIExample/UI/WBP_Inventory');g=B.get_graph(ui,'OnKeyDown')
print([n for n in B.find_node_types(g,'Key',[]) if any(x in n.lower() for x in ['==','equal','name','string','keyevent'])])
