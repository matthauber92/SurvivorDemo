import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC')
for p in ['ImplementedInterfaces','implemented_interfaces']:
    try: print(p,bp.get_editor_property(p))
    except Exception as e:print(str(e))
for n in B.find_nodes(B.get_graph(bp,'EventGraph')):
    if isinstance(n,unreal.K2Node_CustomEvent):
        for p in ['FunctionFlags','CustomFunctionName']:
            try: print(p,n.get_editor_property(p))
            except Exception as e: print(str(e))
        break
print('Editor asset export:', [n for n in dir(unreal) if 'Exporter' in n or 'Import' in n and 'Graph' in n])
