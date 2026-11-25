import unreal,json
from editor_toolset.toolsets.object import ObjectTools as O
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);anim=p.mesh.get_anim_instance();move=p.character_movement
checks={}
def check(n,v):checks[n]=bool(v);print(n,bool(v));assert v,n
def setp(name,value):
 assert O.set_properties(p,json.dumps({name[0].lower()+name[1:]:value}))
setp('PublicSidearm','Weapon.Pistol');setp('PublicActiveSlot',2);setp('PublicAiming',False);setp('PublicReloading',False)
def weight(speed):
 move.set_editor_property('velocity',unreal.Vector(speed,0,0));anim.call_method('UpdatePistolLayer',(1.0,));return anim.get_editor_property('PistolLayerWeight')
p.call_method('NoteHipFire');now=unreal.GameplayStatics.get_time_seconds(w)
check('shot_sets_2_5_second_pose_timeout',abs(p.get_editor_property('PistolPoseUntil')-now-2.5)<.02)
check('recent_shot_keeps_pistol_pose_jogging',weight(350)>.99)
check('recent_shot_keeps_pistol_pose_sprinting',weight(650)>.99)
setp('PistolPoseUntil',now-.1)
check('jog_restores_original_pose_after_timeout',weight(350)<.01)
check('sprint_restores_original_pose_after_timeout',weight(650)<.01)
check('idle_keeps_pistol_pose',weight(0)>.99)
state=p.get_editor_property('CharacterInputState');state.set_editor_property('WantsToSprint',True);state.set_editor_property('WantsToWalk',False);p.set_editor_property('CharacterInputState',state)
normal=p.call_method('GetDesiredGait');print('NORMAL_GAIT',normal)
setp('PublicAiming',True)
aim=p.call_method('GetDesiredGait');print('AIM_GAIT',aim)
check('aim_forces_walk_with_sprint_held',int(aim)==0)
check('aim_keeps_pistol_pose',weight(350)>.99)
setp('PublicAiming',False)
check('release_aim_restores_previous_gait',p.call_method('GetDesiredGait')==normal)
setp('PublicReloading',True);check('reload_keeps_pistol_pose',weight(350)>.99)
setp('PublicReloading',False);setp('PublicActiveSlot',-1);check('holstering_removes_pistol_layer',weight(0)<.01)
Path(unreal.Paths.project_saved_dir(),'pistol-movement-result.json').write_text(json.dumps({'checks':checks,'passed':all(checks.values())},indent=2))
