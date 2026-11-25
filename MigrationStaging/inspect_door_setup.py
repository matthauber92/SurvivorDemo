import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionTestDoor')
print('GRAPHS',B.list_graphs(bp))
print('INTERFACE_APIS',[n for n in dir(unreal.BlueprintEditorLibrary) if 'interface' in n])
print('B_APIS',[n for n in dir(B) if 'interface' in n])
for g in B.list_graphs(bp):
    print(g)
print('INPUT_HELPERS',[n for n in dir(unreal) if 'subsystem' in n.lower() and n.startswith('get')])
print('LIBS',[n for n in dir(unreal) if 'Subsystem' in n or 'EnhancedInput' in n])
