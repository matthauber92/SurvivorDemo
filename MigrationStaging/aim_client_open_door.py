import unreal
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
    pc=unreal.GameplayStatics.get_player_controller(w,0)
    if not pc.has_authority():
        pc.set_control_rotation(unreal.Rotator(pitch=0,yaw=-26.565,roll=0))
