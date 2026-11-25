import unreal,json,time,traceback
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);anim=p.mesh.get_anim_instance();move=p.character_movement;inv=p.get_controller().get_editor_property('InventoryComponent')
assert inv.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_PistolItem'),1))
uid=inv.get_editor_property('BackpackInstances')[0]
assert inv.call_method('TryTransferWeapon',(0,10,uid,inv.get_editor_property('LayoutVersion')))
assert inv.call_method('TrySelectWeapon',(2,uid,inv.get_editor_property('LayoutVersion')))
report={'checks':{},'initial':[p.get_path_name(),str(p.get_editor_property('PublicSidearm')),p.get_editor_property('PublicActiveSlot')]};state={'phase':0,'next':time.monotonic()+.5};out=Path(unreal.Paths.project_saved_dir(),'pistol-movement-result.json')
def check(n,v):report['checks'][n]=bool(v);assert v,n
def weight(speed):
 anim=p.mesh.get_anim_instance()
 move.velocity=unreal.Vector(speed,0,0);anim.call_method('UpdatePistolLayer',(1.0,));return anim.get_editor_property('PistolLayerWeight')
def action(n):return inv.call_method('TryPistolAction',(n,uid,p.get_actor_location(),unreal.Vector(1,0,0)))
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   report['phase0']=[p.get_path_name(),str(p.get_editor_property('PublicSidearm')),p.get_editor_property('PublicActiveSlot'),str(inv.get_editor_property('EquipmentInstances')),str(inv.get_editor_property('ActiveWeaponInstance'))]
   p.call_method('NoteHipFire');now=unreal.GameplayStatics.get_time_seconds(w)
   check('shot_sets_2_5_second_pose_timeout',abs(p.get_editor_property('PistolPoseUntil')-now-2.5)<.02)
   check('recent_shot_keeps_pose_jogging',weight(350)>.99)
   check('recent_shot_keeps_pose_sprinting',weight(650)>.99)
   state['next']=time.monotonic()+2.8
  elif phase==1:
   check('jog_restores_original_pose_after_timeout',weight(350)<.01)
   check('sprint_restores_original_pose_after_timeout',weight(650)<.01)
   check('idle_keeps_pistol_pose',weight(0)>.99)
   inputs=p.get_editor_property('CharacterInputState');inputs.set_editor_property('WantsToSprint',True);inputs.set_editor_property('WantsToWalk',False);p.set_editor_property('CharacterInputState',inputs,unreal.PropertyAccessChangeNotifyMode.NEVER)
   state['normal']=p.call_method('GetDesiredGait');assert action(1)
   check('aim_forces_walk_with_sprint_held',p.call_method('GetDesiredGait').value==0)
   check('aim_keeps_pistol_pose',weight(350)>.99)
   state['next']=time.monotonic()+.5
  elif phase==2:
   check('aim_uses_walking_speed',move.get_editor_property('max_walk_speed')<=p.get_editor_property('WalkSpeeds').x+.1)
   assert action(0)
   check('release_aim_restores_previous_gait',p.call_method('GetDesiredGait')==state['normal'])
   assert inv.call_method('TrySelectWeapon',(2,uid,inv.get_editor_property('LayoutVersion')))
   check('holstering_removes_pistol_layer',weight(0)<.01)
   report['passed']=True;out.write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(movement_test_handle);return
  state['phase']+=1
 except Exception:
  report['passed']=False;report['error']=traceback.format_exc();out.write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(movement_test_handle)
movement_test_handle=unreal.register_slate_post_tick_callback(tick)
