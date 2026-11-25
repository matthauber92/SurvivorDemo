import unreal,json
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();inv=pc.get_editor_property('InventoryComponent');m=p.get_component_by_class(unreal.SkeletalMeshComponent);gun=p.get_editor_property('SidearmVisual')
pc.set_control_rotation(unreal.Rotator(pitch=0,yaw=0,roll=0));inv.call_method('TryPistolAction',(1,inv.get_editor_property('ActiveWeaponInstance'),unreal.Vector(),unreal.Vector(1,0,0)))
print('GUN',gun.get_world_transform(),'MUZZLE',gun.get_socket_transform('Muzzle',unreal.RelativeTransformSpace.RTS_WORLD),'FORWARD',gun.get_forward_vector())
print('HAND',m.get_socket_transform('hand_r',unreal.RelativeTransformSpace.RTS_WORLD),'GRIP',m.get_socket_transform('PistolGrip_R',unreal.RelativeTransformSpace.RTS_WORLD))
print('ANIM',m.get_anim_instance().get_editor_property('PistolAimPitch'))
mesh=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin')
print('SOCKET_API',[n for n in dir(unreal.SkeletalMeshSocket) if 'socket' in n.lower()])
print('NOTES',unreal.load_asset('/Game/AIExample/Combat/Animation/Survivor_AO_Pistol').get_editor_property('sample_data'))
