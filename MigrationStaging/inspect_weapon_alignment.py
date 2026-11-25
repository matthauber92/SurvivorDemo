import unreal
cw=next(w for w in unreal.EditorLevelLibrary.get_pie_worlds(False) if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority());p=unreal.GameplayStatics.get_player_pawn(cw,0)
for name in ['PrimaryVisual','SidearmVisual']:
 c=p.get_editor_property(name);print(name,c.get_editor_property('static_mesh').get_bounds(),c.get_world_transform(),c.get_local_bounds())
m=p.get_component_by_class(unreal.SkeletalMeshComponent)
for name in ['hand_r','weapon_r','VB hand_r_prop_01_Socket','spine_03','pelvis']:print(name,m.get_socket_transform(name,unreal.RelativeTransformSpace.RTS_ACTOR))
