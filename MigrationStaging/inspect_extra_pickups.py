import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);c=p.get_editor_property('InteractionComponent')
print('PAWN',p.get_actor_location())
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Items/BP_ItemPickup.BP_ItemPickup_C')):
 id=str(a.get_editor_property('ItemDefinition').get_editor_property('ItemID'))
 if id in ['Weapon.Revolver','Weapon.Shotgun']:
  m=a.get_editor_property('PickupMesh');s=a.get_editor_property('WeaponInteractionTarget');print(id,'ACTOR',a.get_actor_location(),'MESH',m.get_world_location(),'SPHERE',s.get_world_location(),'SIM',m.is_simulating_physics(),'COLLISION',m.get_collision_enabled(),'TARGET',s.get_collision_enabled(),'VALID',c.call_method('ValidateNearbyPickup',(a,unreal.Vector(1,0,0))))
