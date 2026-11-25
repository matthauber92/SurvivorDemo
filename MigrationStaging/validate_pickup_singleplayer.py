import unreal,json,time,traceback
from pathlib import Path
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
assert len(worlds)==1,'Expected single-player PIE'
w=worlds[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller()
root='/Game/AIExample/Items/'
ic=unreal.load_class(None,root+'BP_InventoryComponent.BP_InventoryComponent_C');pic=unreal.load_class(None,root+'BP_ItemPickup.BP_ItemPickup_C')
inv=pc.get_component_by_class(ic);interact=p.get_component_by_class(unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionComponent.BP_InteractionComponent_C'))
subs=[s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if 'Transient' in s.get_path_name()]
report={'mode':'single-player standalone PIE','checks':{}}
state={'phase':0,'next':time.monotonic()+1}
def check(n,v):report['checks'][n]=bool(v)
def qty(id):return inv.call_method('GetItemQuantity',(unreal.Name(id),))
def inject():
 for s in subs:s.inject_input_vector_for_action(unreal.load_asset('/Game/AIExample/Interaction/IA_SurvivorInteract'),unreal.Vector(1,0,0),[],[])
def move(x,y):p.set_actor_location(unreal.Vector(x,y,90),False,True);pc.set_control_rotation(unreal.Rotator())
def pickup_count():return len(unreal.GameplayStatics.get_all_actors_of_class(w,pic))
move(-180,0)
def finish():
 report['passed']=all(report['checks'].values()) and 'error' not in report
 (Path(unreal.Paths.project_saved_dir())/'PickupValidation/singleplayer-result.json').write_text(json.dumps(report,indent=2))
 unreal.unregister_slate_post_tick_callback(single_pickup_handle)
 unreal.log('SINGLE_PICKUP_RESULT '+json.dumps(report))
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   check('single_world_and_authority',len(worlds)==1 and p.has_authority())
   check('ammo_prompt',str(interact.get_editor_property('PromptText'))=='Press E to collect Handgun Ammo');inject()
  elif phase==1:
   check('ammo_collected',qty('Ammo.Handgun')==30 and pickup_count()==5);move(-180,300)
  elif phase==2:inject()
  elif phase==3:
   check('medkit_collected',qty('Medical.FirstAidKit')==1 and pickup_count()==4);move(-180,-300)
  elif phase==4:inject()
  elif phase==5:
   check('key_collected',qty('Key.Placeholder')==1 and pickup_count()==3)
   before=list(inv.get_editor_property('Quantities'))
   check('invalid_quantity_rejected',not inv.call_method('TryAddItem',(unreal.load_asset(root+'DA_HandgunAmmo'),0)))
   check('capacity_overflow_rejected',not inv.call_method('TryAddItem',(unreal.load_asset(root+'DA_Key'),20)) and list(inv.get_editor_property('Quantities'))==before)
   move(620,0)
  elif phase==6:inject()
  elif phase==7:
   d=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionTestDoor.BP_InteractionTestDoor_C'))[0]
   check('door_still_opens',d.get_editor_property('IsOpen') and abs(d.get_editor_property('DoorHinge').get_editor_property('relative_rotation').yaw-90)<.1)
   finish();return
  state['phase']+=1;state['next']=time.monotonic()+1.2
 except Exception:report['error']=traceback.format_exc();finish()
single_pickup_handle=unreal.register_slate_post_tick_callback(tick)
