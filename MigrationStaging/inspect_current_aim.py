import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);m=p.mesh;gun=p.get_editor_property('SidearmVisual')
print('CONTROL',p.get_controller().get_control_rotation(),'ACTOR',p.get_actor_rotation(),'GUN',gun.get_world_rotation(),'HAND',m.get_socket_transform('hand_r',unreal.RelativeTransformSpace.RTS_WORLD))
print('CORRECT_SOCKET',unreal.MathLibrary.inverse_transform_rotation(m.get_socket_transform('hand_r',unreal.RelativeTransformSpace.RTS_WORLD),unreal.Rotator(pitch=0,yaw=p.get_actor_rotation().yaw,roll=0)))
