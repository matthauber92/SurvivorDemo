import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
root='/Game/AIExample/Items/'
bp=unreal.load_asset(root+'BP_InventoryComponent')
dc=unreal.load_asset(root+'PDA_ItemDefinition').generated_class()
for name,ins,outs,locals in [
 ('GetItemQuantity',[('ItemID','name')],[('Total','int')],[('Count','int')]),
 ('CanAddItem',[('Definition',dc),('Amount','int')],[('CanAdd','bool')],[('FreeSpace','int')]),
 ('TryAddItem',[('Definition',dc),('Amount','int')],[('Added','bool')],[('Remaining','int'),('Transfer','int')])]:
    g=B.get_graph(bp,name) or B.add_function_graph(bp,name)
    for n,t in ins:
        if isinstance(t,str):B.add_function_param(g,n,t,True)
        else:B.add_object_function_param(g,n,t,True)
    for n,t in outs:B.add_function_param(g,n,t,False)
    for n,t in locals:B.add_variable(bp,n,t,graph=g)
    print(name,{n:list(B.find_node_types(g,n,[])) for n,t in locals})
g=B.get_graph(bp,'TryAddItem')
for t in ['Utilities|Array|Get(acopy)','Utilities|Array|SetArrayElem','Utilities|Array|Add','Utilities|Array|Length','Math|Integer|Min(Integer)']:
    print(t,[(p.name,p.type_id) for p in B.get_node_type_pins(g,t).input_pins])
B.compile_blueprint(bp);unreal.EditorAssetLibrary.save_loaded_asset(bp)
