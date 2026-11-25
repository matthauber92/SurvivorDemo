import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Character) if 'Survivor' in p.get_class().get_name());anim=p.mesh.get_anim_instance()
for n in ['PublicActiveSlot','PublicSidearm','PublicAiming','PublicReloading']:print(n,p.get_editor_property(n))
print('ID',p.call_method('GetActiveFirearmID'),'ANIM',anim.get_class().get_path_name())
for n in ['PistolLayerWeight','UseShotgunPose']:print(n,anim.get_editor_property(n))
print('OWNER',anim.try_get_pawn_owner(),'VEL',p.get_velocity())
anim.call_method('UpdatePistolLayer',(1.0,));print('WEIGHT_AFTER',anim.get_editor_property('PistolLayerWeight'))
for b in ['hand_r','index_01_r','middle_01_r','thumb_01_r','RevolverGrip_R']:print(b,p.mesh.get_socket_transform(b,unreal.RelativeTransformSpace.RTS_WORLD))
