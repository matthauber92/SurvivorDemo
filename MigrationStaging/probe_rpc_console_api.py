import unreal
print(unreal.ConsoleVariablesEditorAssetSaveData.__doc__)
print([n for n in dir(unreal.ConsoleVariablesEditorFunctionLibrary) if 'exec' in n])
print(unreal.ConsoleVariablesEditorFunctionLibrary.execute_console_command.__doc__ if hasattr(unreal.ConsoleVariablesEditorFunctionLibrary,'execute_console_command') else '')
print([n for n in dir(unreal.ConsoleVariablesEditorAssetSaveData) if not n.startswith('_')])
