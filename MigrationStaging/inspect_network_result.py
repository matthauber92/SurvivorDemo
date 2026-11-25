import unreal
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
    for d in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionTestDoor.BP_InteractionTestDoor_C')):
        print('DOOR',d.has_authority(),d.get_editor_property('IsOpen'),d.get_editor_property('DoorHinge').get_editor_property('relative_rotation'))
for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem):
    print('SUBSYS',s.get_path_name())

