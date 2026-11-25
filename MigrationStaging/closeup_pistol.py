import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];d=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.DebugCameraController)[0]
p=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Character) if 'Survivor' in p.get_class().get_name());m=p.get_component_by_class(unreal.SkeletalMeshComponent)
target=m.get_socket_location('hand_r')+unreal.Vector(0,0,-8);location=target+unreal.Vector(35,70,5)
print('PAWN',d.get_controlled_pawn(),d.get_spectator_pawn())
d.set_actor_location(location,False,True);d.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(location,target))
if d.get_spectator_pawn():d.get_spectator_pawn().set_actor_location(location,False,True)
unreal.SystemLibrary.execute_console_command(w,'showdebug reset',d)
