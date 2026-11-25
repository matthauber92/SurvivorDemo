import unreal
print('DUP',[n for n in dir(unreal) if any(t in n.lower() for t in ['duplicate','importobject','textfactory'])])
print('GRAPH',[n for n in dir(unreal.BlueprintGraphEditor) if not n.startswith('_')])
print('NODE',[n for n in dir(unreal.K2Node_CustomEvent) if any(t in n for t in ['dup','copy','import','name','prop'])])
