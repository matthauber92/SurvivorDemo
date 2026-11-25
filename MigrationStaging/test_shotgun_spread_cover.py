import unreal,time,json,traceback
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();inv=pc.get_editor_property('InventoryComponent');uid=inv.get_editor_property('EquipmentInstances')[0]
if str(inv.get_editor_property('ActiveWeaponInstance'))!=str(uid):assert inv.call_method('TrySelectWeapon',(0,uid,inv.get_editor_property('LayoutVersion')))
p.set_actor_location(unreal.Vector(0,0,4000),False,True);p.character_movement.set_movement_mode(unreal.MovementMode.MOVE_FLYING);pc.set_control_rotation(unreal.Rotator());assert inv.call_method('TryPistolAction',(1,uid,p.get_actor_location(),unreal.Vector(1,0,0)))
target=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Combat/BP_PistolTarget.BP_PistolTarget_C'))[0]
mesh=target.get_editor_property('TargetMesh');mesh.set_world_scale3d(unreal.Vector(1,10,10))
block=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor) if a.static_mesh_component.get_editor_property('static_mesh')==unreal.load_asset('/Engine/BasicShapes/Cube'));old=block.get_actor_transform();block.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE);block.static_mesh_component.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_BLOCK)
report={'checks':{}};state={'phase':0,'next':time.monotonic()+1};out=Path(unreal.Paths.project_saved_dir())/'shotgun-spread-cover-result.json'
def check(n,b):report['checks'][n]=bool(b);assert b,n
def fire():p.call_method('PerformPistolShot',(p.get_actor_location()+unreal.Vector(0,0,50),unreal.Vector(1,0,0)))
def finish():
 block.set_actor_transform(old,False,True);report['passed']='error' not in report and all(report['checks'].values());out.write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(spread_cover_handle)
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   target.set_actor_location(unreal.Vector(2000,0,4050),False,True);fire();health=target.get_editor_property('Health');report['far_health']=health
   check('falloff_reduces_damage_at_20m',0<health<100)
   ends=list(p.get_editor_property('PublicShotEnds'));check('eight_pellets',len(ends)==8);check('cone_has_area',max(e.y for e in ends)-min(e.y for e in ends)>150)
   state['health']=health
  elif phase==1:
   block.set_actor_location(unreal.Vector(1000,0,4050),False,True);block.set_actor_scale3d(unreal.Vector(.2,10,10));fire();check('cover_blocks_all_pellets',abs(target.get_editor_property('Health')-state['health'])<.01)
   block.set_actor_transform(old,False,True)
   target.set_actor_location(unreal.Vector(3500,0,4050),False,True);fire();check('beyond_30m_no_damage',abs(target.get_editor_property('Health')-state['health'])<.01)
   target.set_actor_location(unreal.Vector(500,0,4050),False,True);fire();check('close_range_lethal',target.get_editor_property('Health')<=0)
   anim=p.mesh.get_anim_instance();check('rifle_hold_selected',anim.get_editor_property('UseShotgunPose'))
   inv.call_method('TryPistolAction',(0,uid,p.get_actor_location(),unreal.Vector(1,0,0)));p.call_method('NoteHipFire');p.character_movement.velocity=unreal.Vector(350,0,0);anim.call_method('UpdatePistolLayer',(1.0,));check('recent_shot_keeps_hold',anim.get_editor_property('PistolLayerWeight')>.99);state['next']=time.monotonic()+2.8
  elif phase==2:
   p.character_movement.velocity=unreal.Vector(350,0,0);anim=p.mesh.get_anim_instance();anim.call_method('UpdatePistolLayer',(1.0,));check('normal_run_after_2_5_seconds',anim.get_editor_property('PistolLayerWeight')<.01)
   finish();return
  state['phase']+=1
  if phase!=1:state['next']=time.monotonic()+.6
 except Exception:report['error']=traceback.format_exc();finish()
spread_cover_handle=unreal.register_slate_post_tick_callback(tick)
