import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];pc=unreal.GameplayStatics.get_player_controller(w,0);p=unreal.GameplayStatics.get_player_pawn(w,0)
comp=p.get_component_by_class(unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionComponent').generated_class())
print('PAWN',p.get_actor_location(),'CAMERA',pc.player_camera_manager.get_camera_location(),pc.player_camera_manager.get_camera_rotation(),'CONTROL',pc.get_control_rotation())
print('FOCUS',comp.get_editor_property('FocusedActor'),comp.get_editor_property('PromptText'))
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_asset('/Game/AIExample/Items/BP_ItemPickup').generated_class()):
 if str(a.get_editor_property('ItemDefinition').get_editor_property('ItemID'))=='Weapon.Pistol':
  m=a.get_editor_property('PickupMesh');print('PISTOL',a.get_actor_location(),'MESH',m.get_world_location(),'VIS',m.get_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY),'PROMPT',a.call_method('GetInteractionPrompt',(p,)))
