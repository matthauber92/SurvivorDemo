import unreal,time,json,traceback
from pathlib import Path
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
sw=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority());cw=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
cp=unreal.GameplayStatics.get_player_pawn(cw,0);cpc=cp.get_controller();ci=cpc.get_editor_property('InventoryComponent');comp=cp.get_editor_property('InteractionComponent')
rp=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(sw,cp.get_class()) if not p.is_locally_controlled());ri=rp.get_controller().get_editor_property('InventoryComponent')
cls=unreal.load_class(None,'/Game/AIExample/Items/BP_ItemPickup.BP_ItemPickup_C')
def guns(w):return [a for a in unreal.GameplayStatics.get_all_actors_of_class(w,cls) if str(a.get_editor_property('ItemDefinition').get_editor_property('ItemID'))=='Weapon.Pistol']
gun=guns(sw)[0];center=gun.get_actor_location();report={'checks':{}};state={'phase':0,'aim':0,'next':time.monotonic()+1}
def check(n,b):report['checks'][n]=bool(b);assert b,n
def finish():
 report['passed']=all(report['checks'].values()) and 'error' not in report
 (Path(unreal.Paths.project_saved_dir())/'PistolAdjustmentValidation/multiplayer-result.json').write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(pistol_multi_handle)
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   rp.set_actor_location(center+unreal.Vector(-140,0,88),False,True)
   cg=min(guns(cw),key=lambda a:(a.get_actor_location()-center).length());state['clientgun']=cg
   s=cg.get_editor_property('WeaponInteractionTarget')
   check('client_has_generous_trace_target',abs(s.get_scaled_sphere_radius()-32)<.1 and s.get_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY)==unreal.CollisionResponseType.ECR_BLOCK)
  elif phase==1:
   cam=unreal.GameplayStatics.get_player_camera_manager(cw,0);cpc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(cam.get_camera_location(),center+unreal.Vector(0,20,10)))
   state['aim']+=1
   if state['aim']<12:state['next']=time.monotonic()+.15;return
  elif phase==2:
   check('remote_client_gets_off_center_prompt',comp.get_editor_property('FocusedActor')==state['clientgun'] and 'Pistol' in str(comp.get_editor_property('PromptText')))
   for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem):
    if 'Transient' in s.get_path_name():s.inject_input_vector_for_action(unreal.load_asset('/Game/AIExample/Interaction/IA_SurvivorInteract'),unreal.Vector(1,0,0),[],[])
  elif phase==3:
   check('client_E_collects_on_authority',len(ri.get_editor_property('WeaponInstances'))==len(ci.get_editor_property('WeaponInstances'))==1)
   check('pickup_despawns_on_both',len(guns(sw))==len(guns(cw))==1)
   uid=ri.get_editor_property('BackpackInstances')[0];assert ri.call_method('TryTransferWeapon',(0,10,uid,ri.get_editor_property('LayoutVersion')))
  elif phase==4:
   r=cp.get_editor_property('SidearmVisual').get_editor_property('relative_rotation')
   check('hip_alignment_replicates',abs(r.roll+90)<.1 and abs(abs(r.yaw)-180)<.1)
   assert ri.call_method('TrySelectWeapon',(2,ri.get_editor_property('EquipmentInstances')[2],ri.get_editor_property('LayoutVersion')))
  elif phase==5:
   pos=cp.get_editor_property('SidearmVisual').get_editor_property('relative_location')
   check('hand_alignment_replicates',(pos-unreal.Vector(-13,2,3)).length()<.1)
   finish();return
  state['phase']+=1;state['next']=time.monotonic()+.8
 except Exception:report['error']=traceback.format_exc();finish()
pistol_multi_handle=unreal.register_slate_post_tick_callback(tick)
