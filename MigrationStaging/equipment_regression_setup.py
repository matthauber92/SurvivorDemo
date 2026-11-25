import unreal,json
ls=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert ls.load_level('/Game/AIExample/Maps/Lvl_PickupTest')
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for a in actors.get_all_level_actors():
 if a.get_actor_label() in ['Equipment_0','Equipment_1','Equipment_2','Equipment_3']:actors.destroy_actor(a)
assert ls.save_current_level()
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.LevelEditorPlaySettings'))
unreal.ToolsetLibrary.set_object_properties(s,json.dumps({'playNetMode':'PIE_Standalone','playNumberOfClients':1,'runUnderOneProcess':True}))
print('REGRESSION_MAP_READY')
