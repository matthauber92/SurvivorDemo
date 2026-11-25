import unreal
print('EDITORPY',[n for n in dir(unreal.EditorPythonScripting) if not n.startswith('_')])
print('CVASSET',[n for n in dir(unreal.ConsoleVariablesAsset) if any(x in n for x in ['exec','command'])])
print(unreal.ConsoleVariablesAsset.execute_saved_commands.__doc__)
