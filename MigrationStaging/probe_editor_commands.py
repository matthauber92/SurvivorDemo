import unreal
for name in ['EditorLevelLibrary','EditorUtilityLibrary','ToolsetLibrary','UnrealEditorSubsystem','EditorPythonScriptingLibrary']:
    cls=getattr(unreal,name,None)
    if cls: print(name,[n for n in dir(cls) if any(x in n.lower() for x in ['console','exec','command','interface','import','text'])])
print([n for n in dir(unreal) if 'Console' in n or 'Automation' in n])
print({n:str(getattr(unreal.ConsoleVariablesEditorFunctionLibrary,n).__doc__) for n in dir(unreal.ConsoleVariablesEditorFunctionLibrary) if 'execute' in n or 'console' in n})
for name in ['EditorAutomationObject','EditorAutomationActor','AutomationLibrary','ConsoleVariablesAsset','KismetSystemLibrary']:
    cls=getattr(unreal,name,None)
    if cls:print(name,{n:str(getattr(cls,n).__doc__) for n in dir(cls) if any(x in n.lower() for x in ['console','exec','command','interface','import','text'])})
