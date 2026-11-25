import unreal,time,json,traceback
from pathlib import Path
w=next(w for w in unreal.EditorLevelLibrary.get_pie_worlds(False) if unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
pawn=unreal.GameplayStatics.get_player_pawn(w,0)
gun=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_asset('/Game/AIExample/Items/BP_ItemPickup').generated_class()) if str(a.get_editor_property('ItemDefinition').get_editor_property('ItemID'))=='Weapon.Pistol')
m=gun.get_editor_property('PickupMesh');origin=gun.get_actor_location()
pawn.set_actor_location(unreal.Vector(origin.x-180,origin.y,88.2),False,True);pawn.get_controller().set_control_rotation(unreal.Rotator())
state={'start':time.monotonic()+1,'samples':[]};report={'checks':{'pawn_ignored':m.get_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN)==unreal.CollisionResponseType.ECR_IGNORE,'foot_trace_ignored':m.get_collision_response_to_channel(unreal.CollisionChannel.ECC_CAMERA)==unreal.CollisionResponseType.ECR_IGNORE,'pickup_trace_still_blocked':m.get_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY)==unreal.CollisionResponseType.ECR_BLOCK}}
def tick(dt):
 now=time.monotonic()
 if now<state['start']:return
 if now-state['start']<1.5:
  pawn.add_movement_input(unreal.Vector(1,0,0),1,False);state['samples'].append(pawn.get_actor_location().z);return
 report['checks']['walked_across_weapon']=pawn.get_actor_location().x>origin.x+50
 report['checks']['no_capsule_bounce']=max(state['samples'])-min(state['samples'])<5
 report['checks']['weapon_not_kicked']=(gun.get_actor_location()-origin).length()<3
 report['height_range']=max(state['samples'])-min(state['samples']);report['weapon_displacement']=(gun.get_actor_location()-origin).length();report['passed']=all(report['checks'].values())
 (Path(unreal.Paths.project_saved_dir())/'EquipmentValidation/walkover-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));unreal.unregister_slate_post_tick_callback(walk_handle)
walk_handle=unreal.register_slate_post_tick_callback(tick)
