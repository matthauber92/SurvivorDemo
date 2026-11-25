import unreal,time,builtins
keyboard_samples=list(builtins.interaction_keyboard_record[1]) if hasattr(builtins,'interaction_keyboard_record') else []
keyboard_doors=[]
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
    d=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionTestDoor.BP_InteractionTestDoor_C'))[0]
    keyboard_doors.append(d)
def record_keyboard_tick(dt):
    if not unreal.EditorLevelLibrary.get_pie_worlds(False):
        unreal.unregister_slate_post_tick_callback(keyboard_record_handle)
        return
    sample={'time':time.monotonic(),'doors':[{'authority':d.has_authority(),'open':d.get_editor_property('IsOpen'),'yaw':d.get_editor_property('DoorHinge').get_editor_property('relative_rotation').yaw} for d in keyboard_doors]}
    if len(keyboard_samples)<20000:keyboard_samples.append(sample)
keyboard_record_handle=unreal.register_slate_post_tick_callback(record_keyboard_tick)
builtins.interaction_keyboard_record=(keyboard_record_handle,keyboard_samples,keyboard_doors)
print('RECORDING_REAL_KEYBOARD_ANIMATION')
