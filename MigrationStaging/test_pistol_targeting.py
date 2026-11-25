import unreal,json,time,traceback
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller()
inv=pc.get_editor_property('InventoryComponent');comp=p.get_editor_property('InteractionComponent')
guns=[a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Items/BP_ItemPickup.BP_ItemPickup_C')) if str(a.get_editor_property('ItemDefinition').get_editor_property('ItemID'))=='Weapon.Pistol']
gun=guns[0];center=gun.get_actor_location();sphere=gun.get_editor_property('WeaponInteractionTarget');mesh=gun.get_editor_property('PickupMesh')
out=Path(unreal.Paths.project_saved_dir())/'PistolAdjustmentValidation';out.mkdir(exist_ok=True)
report={'checks':{}};state={'phase':0,'next':time.monotonic()+.8,'aim':0}
def check(n,b):report['checks'][n]=bool(b);assert b,n
def finish():
 report['passed']=all(report['checks'].values()) and 'error' not in report
 (out/'targeting-result.json').write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(pistol_target_handle)
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   check('target_follows_physics_mesh',sphere.get_attach_parent()==mesh and (sphere.get_world_location()-gun.get_actor_location()).length()<1)
   check('generous_query_only_target',sphere.get_collision_enabled()==unreal.CollisionEnabled.QUERY_ONLY and abs(sphere.get_scaled_sphere_radius()-32)<.1)
   check('pawn_and_camera_ignore_target',all(sphere.get_collision_response_to_channel(ch)==unreal.CollisionResponseType.ECR_IGNORE for ch in [unreal.CollisionChannel.ECC_PAWN,unreal.CollisionChannel.ECC_CAMERA]))
   check('gun_remains_physical',mesh.is_simulating_physics() and mesh.get_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN)==unreal.CollisionResponseType.ECR_IGNORE)
   p.set_actor_location(center+unreal.Vector(-140,0,88),False,True)
  elif phase==1:
   origin=center+unreal.Vector(-340,0,160)
   results=[]
   for dy,dz in [(0,0),(-20,0),(20,0),(0,20),(-15,15),(15,15)]:
    aim=center+unreal.Vector(0,dy,dz);direction=(aim-origin).normal()
    results.append(bool(comp.call_method('ValidateTarget',(gun,origin,direction))))
   report['offset_aim_results']=results;check('off_center_aim_is_accepted',all(results))
   check('wrong_direction_rejected',not comp.call_method('ValidateTarget',(gun,origin,unreal.Vector(-1,0,0))))
   check('spoofed_view_origin_rejected',not comp.call_method('ValidateTarget',(gun,origin+unreal.Vector(-1000,0,0),(center-origin).normal())))
   blocks=[a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor) if a.static_mesh_component.get_editor_property('static_mesh')==unreal.load_asset('/Engine/BasicShapes/Cube')]
   if blocks:
    block=blocks[0];old=block.get_actor_transform();block.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE);block.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS);block.static_mesh_component.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_BLOCK);block.set_actor_location(center+unreal.Vector(-65,0,70),False,True);block.set_actor_scale3d(unreal.Vector(.15,1,2))
    check('wall_still_blocks_pickup',not comp.call_method('ValidateTarget',(gun,origin,(center-origin).normal())))
    block.set_actor_transform(old,False,True)
   p.set_actor_location(center+unreal.Vector(-500,0,88),False,True)
   check('out_of_range_rejected',not comp.call_method('ValidateTarget',(gun,origin,(center-origin).normal())))
   p.set_actor_location(center+unreal.Vector(-140,0,88),False,True)
  elif phase==2:
   camera=unreal.GameplayStatics.get_player_camera_manager(w,0)
   pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(camera.get_camera_location(),center+unreal.Vector(0,20,10)))
   state['aim']+=1
   if state['aim']<12:state['next']=time.monotonic()+.15;return
  elif phase==3:
   comp.call_method('UpdateFocus');report['prompt']=str(comp.get_editor_property('PromptText'))
   check('actual_camera_gets_off_center_prompt',comp.get_editor_property('FocusedActor')==gun and 'Pistol' in report['prompt'])
   state['count']=inv.call_method('GetItemQuantity',(unreal.Name('Weapon.Pistol'),))
   for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem):
    if 'Transient' in s.get_path_name():s.inject_input_vector_for_action(unreal.load_asset('/Game/AIExample/Interaction/IA_SurvivorInteract'),unreal.Vector(1,0,0),[],[])
  elif phase==4:
   check('E_collects_from_off_center_aim',inv.call_method('GetItemQuantity',(unreal.Name('Weapon.Pistol'),))==state['count']+1)
   check('pickup_removed_once',len([a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Items/BP_ItemPickup.BP_ItemPickup_C')) if str(a.get_editor_property('ItemDefinition').get_editor_property('ItemID'))=='Weapon.Pistol'])==len(guns)-1)
   finish();return
  state['phase']+=1;state['next']=time.monotonic()+.6
 except Exception:report['error']=traceback.format_exc();finish()
pistol_target_handle=unreal.register_slate_post_tick_callback(tick)

