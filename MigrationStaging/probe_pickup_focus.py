import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();c=p.get_editor_property('InteractionComponent')
pickups=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Items/BP_ItemPickup.BP_ItemPickup_C'))
for a in pickups:
 loc=a.get_actor_location();p.set_actor_location(loc+unreal.Vector(-160,0,90),False,True)
 for distance in [250,350,600]:
  origin=p.get_actor_location()+unreal.Vector(-distance,65,45);direction=unreal.MathLibrary.normal(loc-origin)
  print('VALID',a.get_name(),distance,c.call_method('ValidateTarget',(a,origin,direction)))
 print('COMPONENTS',[(x.get_name(),str(x.get_world_location()),str(x.get_collision_enabled())) for x in a.get_components_by_class(unreal.PrimitiveComponent)])
 print('TRY',a.call_method('TryInteract',(p,)))
