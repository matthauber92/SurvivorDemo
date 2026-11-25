import unreal
cw=next(w for w in unreal.EditorLevelLibrary.get_pie_worlds(False) if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority());p=unreal.GameplayStatics.get_player_pawn(cw,0)
for n,z in [('PrimaryVisual',-12),('SecondaryVisual',12)]:
 c=p.get_editor_property(n);c.set_relative_location(unreal.Vector(10,-18,z),False,True);c.set_relative_rotation(unreal.Rotator(0,0,0),False,True)
c=p.get_editor_property('SidearmVisual');c.attach_to_component(p.get_component_by_class(unreal.SkeletalMeshComponent),'hand_r',unreal.AttachmentRule.SNAP_TO_TARGET,unreal.AttachmentRule.SNAP_TO_TARGET,unreal.AttachmentRule.SNAP_TO_TARGET,False);c.set_relative_location(unreal.Vector(-4,0,5),False,True);c.set_relative_rotation(unreal.Rotator(0,180,0),False,True)
unreal.AutomationLibrary.take_high_res_screenshot(1280,900,'WeaponAlignment')
