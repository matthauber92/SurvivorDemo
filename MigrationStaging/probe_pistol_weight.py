import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0)
p.call_method('SetWeaponPresentation',(unreal.Name('None'),unreal.Name('None'),unreal.Name('Weapon.Pistol'),2))
p.call_method('NoteHipFire');a=p.mesh.get_anim_instance()
print('OWNER',a.try_get_pawn_owner()==p,'STATE',p.get_editor_property('PublicActiveSlot'),p.get_editor_property('PublicSidearm'),p.get_editor_property('PistolPoseUntil'))
print('BEFORE',a.get_editor_property('PistolLayerWeight'))
a.call_method('UpdatePistolLayer',(1.0,))
print('AFTER',a.get_editor_property('PistolLayerWeight'),'STATE',p.get_editor_property('PublicActiveSlot'),p.get_editor_property('PublicSidearm'))
