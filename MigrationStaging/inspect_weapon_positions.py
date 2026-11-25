import unreal
cw=next(w for w in unreal.EditorLevelLibrary.get_pie_worlds(False) if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority());p=unreal.GameplayStatics.get_player_pawn(cw,0)
for c in p.get_components_by_class(unreal.SceneComponent):
 if isinstance(c,(unreal.SkeletalMeshComponent,unreal.StaticMeshComponent,unreal.ChildActorComponent)):
  print('COMP',c.get_name(),c.get_world_location(),c.is_visible(),c.get_editor_property('hidden_in_game'),c.get_attach_socket_name())
  if isinstance(c,unreal.SkeletalMeshComponent):print('SOCKET',c.get_socket_location('hand_r'),c.get_socket_location('spine_03'),c.get_editor_property('visibility_based_anim_tick_option'))
  if isinstance(c,unreal.ChildActorComponent):
   ch=c.get_editor_property('child_actor');print('CHILD',ch)
   if ch:
    for sk in ch.get_components_by_class(unreal.SkeletalMeshComponent):print('CHILD_SKEL',sk.get_name(),sk.get_socket_location('hand_r'),sk.get_socket_location('spine_03'),sk.is_visible())

