import unreal,time,json,traceback
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();inv=pc.get_editor_property('InventoryComponent');c=p.get_editor_property('InteractionComponent')
cls=unreal.load_class(None,'/Game/AIExample/Items/BP_ItemPickup.BP_ItemPickup_C')
gun=min([a for a in unreal.GameplayStatics.get_all_actors_of_class(w,cls) if str(a.get_editor_property('ItemDefinition').get_editor_property('ItemID'))=='Weapon.Shotgun'],key=lambda a:a.get_actor_location().y)
gun.set_actor_location(unreal.Vector(1200,-400,40),False,True)
center=gun.get_actor_location();p.set_actor_location(center+unreal.Vector(-140,0,88),False,True);pc.set_control_rotation(unreal.Rotator(0,0,0))
report={'checks':{}};state={'phase':0,'next':time.monotonic()+1};out=Path(unreal.Paths.project_saved_dir())/'nearby-shotgun-result.json'
def check(n,b):
 report['checks'][n]=bool(b);assert b,n
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase'];cam=unreal.GameplayStatics.get_player_camera_manager(w,0)
  if phase==0:
   c.call_method('UpdateFocus');report['prompt']=str(c.get_editor_property('PromptText'))
   check('level_camera_focuses_floor_shotgun',c.get_editor_property('FocusedActor')==gun)
   check('shotgun_prompt_visible','Shotgun' in report['prompt'])
   check('off_center_nearby_valid',c.call_method('ValidateNearbyPickup',(gun,unreal.Vector(1,0,0))))
   check('behind_player_rejected',not c.call_method('ValidateNearbyPickup',(gun,unreal.Vector(-1,0,0))))
   p.set_actor_location(center+unreal.Vector(-350,0,88),False,True)
   check('out_of_range_rejected',not c.call_method('ValidateNearbyPickup',(gun,unreal.Vector(1,0,0))))
   p.set_actor_location(center+unreal.Vector(-140,0,88),False,True)
   block=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor) if a.static_mesh_component.get_editor_property('static_mesh')==unreal.load_asset('/Engine/BasicShapes/Cube'))
   old=block.get_actor_transform();block.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE)
   block.set_actor_location(center+unreal.Vector(-65,0,100),False,True);block.set_actor_scale3d(unreal.Vector(.1,1,2))
   block.static_mesh_component.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_BLOCK)
   check('wall_blocks_nearby_pickup',not c.call_method('ValidateNearbyPickup',(gun,unreal.Vector(1,0,0))))
   block.set_actor_transform(old,False,True)
   state['count']=inv.call_method('GetItemQuantity',(unreal.Name('Weapon.Shotgun'),))
  elif phase==1:
   for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem):
    if 'Transient' in s.get_path_name():s.inject_input_vector_for_action(unreal.load_asset('/Game/AIExample/Interaction/IA_SurvivorInteract'),unreal.Vector(1,0,0),[],[])
  elif phase==2:
   check('interact_input_collects_shotgun',inv.call_method('GetItemQuantity',(unreal.Name('Weapon.Shotgun'),))==state['count']+1)
   check('shotgun_removed',gun not in unreal.GameplayStatics.get_all_actors_of_class(w,cls))
   report['passed']=True;out.write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(nearby_test_handle);return
  state['phase']+=1;state['next']=time.monotonic()+.6
 except Exception:
  report['error']=traceback.format_exc();report['passed']=False;out.write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(nearby_test_handle)
nearby_test_handle=unreal.register_slate_post_tick_callback(tick)
