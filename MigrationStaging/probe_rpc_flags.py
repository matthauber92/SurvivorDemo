import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');g=B.get_graph(bp,'EventGraph')
for n in B.find_nodes(g):
 if isinstance(n,unreal.K2Node_CustomEvent) and 'ServerPistolAction' in B._get_node_info(n).type_id:
  for prop in ['function_flags','FunctionFlags','custom_function_name']:
   try:print(prop,n.get_editor_property(prop))
   except Exception as e:print(prop,str(e))
 if n.get_name()=='K2Node_CallFunction_33':print('SERVERCALL',B._get_node_info(n))
print('BLUEPRINTLIB', [n for n in dir(unreal.BlueprintEditorLibrary) if any(s in n for s in ['net','rep','function','event'])])
