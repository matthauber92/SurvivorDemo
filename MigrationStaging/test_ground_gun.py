import unreal,json,time,traceback
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];pc=unreal.GameplayStatics.get_player_controller(w,0);pawn=unreal.GameplayStatics.get_player_pawn(w,0)
print('WORLD',w.get_path_name(),'CONTROLLER',pc.get_class().get_name())
cls=unreal.load_asset('/Game/AIExample/Items/BP_ItemPickup').generated_class()
guns=[a for a in unreal.GameplayStatics.get_all_actors_of_class(w,cls) if str(a.get_editor_property('ItemDefinition').get_editor_property('ItemID'))=='Weapon.Pistol']
gun=guns[0];mesh=gun.get_editor_property('PickupMesh');p=gun.get_actor_location()
print('GUNS',[(str(a.get_actor_location()),a.get_editor_property('PickupMesh').is_simulating_physics(),str(a.get_actor_scale3d())) for a in guns])
report={'checks':{},'initial_z':p.z};state={'phase':0,'next':time.monotonic()+.3}
def check(n,b):report['checks'][n]=bool(b)
def finish():
 report['passed']=all(report['checks'].values());(Path(unreal.Paths.project_saved_dir())/'EquipmentValidation/ground-gun-result.json').write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(ground_gun_handle);print(json.dumps(report))
check('mesh_is_actor_root',gun.root_component==mesh);check('gun_physics_enabled',mesh.is_simulating_physics())
check('gun_on_ground',-2<p.z<20)
gun.set_actor_location(p+unreal.Vector(0,0,100),False,True);mesh.wake_all_rigid_bodies()
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   check('gravity_moves_gun_down',gun.get_actor_location().z<p.z+95);state['next']=time.monotonic()+2
  elif phase==1:
   check('gun_settles_above_floor',-2<gun.get_actor_location().z<20)
   q=gun.get_actor_location();pawn.set_actor_location(unreal.Vector(q.x-120,q.y,90),False,True);pc.set_control_rotation(unreal.Rotator(-35,0,0));state['next']=time.monotonic()+1
  elif phase<25:
   center,extent,radius=unreal.SystemLibrary.get_component_bounds(mesh)
   pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(pc.player_camera_manager.get_camera_location(),center));state['next']=time.monotonic()+.25
  else:
   comp=pawn.get_component_by_class(unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionComponent').generated_class());comp.call_method('UpdateFocus')
   report['prompt']=str(comp.get_editor_property('PromptText'));report['gun_location']=str(gun.get_actor_location())
   check('ground_pistol_focused',comp.get_editor_property('FocusedActor')==gun);check('pickup_prompt',report['prompt']=='Press E to collect Pistol');finish();return
  state['phase']+=1
 except Exception:report['error']=traceback.format_exc();check('no_test_exception',False);finish()
ground_gun_handle=unreal.register_slate_post_tick_callback(tick)
