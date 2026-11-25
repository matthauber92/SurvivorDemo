import unreal
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
    pc=unreal.GameplayStatics.get_player_controller(w,0)
    if pc.has_authority():
        pc.set_control_rotation(unreal.Rotator(pitch=0,yaw=-26.565,roll=0))
        d=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionTestDoor.BP_InteractionTestDoor_C'))[0]
        print('DOOR_PANEL',d.get_editor_property('DoorPanel').get_world_location())
        print('PC_ROTATION',pc.get_control_rotation())
