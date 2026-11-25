import unreal
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
for w in worlds:
    print('WORLD',w.get_name())
    for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Pawn):
        print('PAWN',p.get_name(),'authority',p.has_authority(),'local',p.is_locally_controlled(),'role',p.get_local_role())
        if p.has_authority():
            p.set_actor_location(unreal.Vector(-600,300,90) if p.is_locally_controlled() else unreal.Vector(-180,0,90),False,True)
    pc=unreal.GameplayStatics.get_player_controller(w,0)
    if pc: pc.set_control_rotation(unreal.Rotator(0,0,0))
print(unreal.EnhancedInputLocalPlayerSubsystem.inject_input_vector_for_action.__doc__)
print([n for n in dir(unreal) if 'LocalPlayer' in n])
print([n for n in dir(unreal) if 'Subsystem' in n and 'Library' in n])
print([n for n in dir(unreal.PlayerController) if 'local_player' in n or 'subsystem' in n])
