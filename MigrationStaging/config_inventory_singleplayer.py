import unreal,json
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.LevelEditorPlaySettings'))
unreal.ToolsetLibrary.set_object_properties(s,json.dumps({'playNetMode':'PIE_Standalone','playNumberOfClients':1,'runUnderOneProcess':True,'newWindowWidth':1280,'newWindowHeight':800}))
