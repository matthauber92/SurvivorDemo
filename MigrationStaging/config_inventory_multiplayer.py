import unreal,json
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.LevelEditorPlaySettings'))
assert unreal.ToolsetLibrary.set_object_properties(s,json.dumps({'playNetMode':'PIE_ListenServer','playNumberOfClients':2,'runUnderOneProcess':True,'newWindowWidth':960,'newWindowHeight':720}))
