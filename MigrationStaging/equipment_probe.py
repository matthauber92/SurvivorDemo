import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Items/BP_InventoryComponent');g=B.get_graph(bp,'TryAddItem')
r={t:list(B.find_node_types(g,t,[])) for t in ['NewGuid','ToString(Guid)','FindItem','RemoveIndex','GetEquipmentType']}
print(json.dumps(r))
print('override',B.add_function_graph.__doc__)
