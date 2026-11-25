import unreal,sys,datetime,shutil
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from weapon_extension_helpers import *
from editor_toolset.toolsets.blueprint import _BlueprintCache
from editor_toolset.toolsets.object import ObjectTools as O
root=Path(unreal.Paths.project_dir()); backup=root/'Backups'/('RecoilTurning-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir(parents=True)
for rel in ['AIExample/Interaction/BP_SurvivorInteractionCharacter','Blueprints/SandboxCharacter_CMC_ABP','AIExample/Combat/Animation/Survivor_MM_Rifle_Fire']:
 shutil.copy2(root/'Content'/(rel+'.uasset'),backup/(rel.split('/')[-1]+'.uasset'))
bp=asset('Interaction/BP_SurvivorInteractionCharacter')
write(bp,'NoteHipFire','''(fn NoteHipFire ()
 (Variables|Default|SetHipFireUntil (+ (Utilities|Time|GetGameTimeinSeconds) 1.0))
 (Variables|Default|SetPistolPoseUntil (+ (Utilities|Time|GetGameTimeinSeconds) 2.5)))''')
# Apply bounded armed idle facing from the existing per-frame camera update.
if B.get_graph(bp,'UpdateRotation_PreCMC'): B.remove_function_graph(bp,'UpdateRotation_PreCMC')
fn(bp,'UpdateArmedIdleFacing',[('DeltaSeconds','float')])
write(bp,'UpdateArmedIdleFacing',f'''(fn UpdateArmedIdleFacing (DeltaSeconds)
 (if (and {supported('(CallFunction|GetActiveFirearmID)')} (< (Math|Vector|VectorLengthXY (Transformation|GetVelocity)) 150.0))
  (bind (Roll Pitch Yaw) (Math|Rotator|BreakRotator (Pawn|GetBaseAimRotation)))
  (Transformation|SetActorRotation :NewRotation (Math|Interpolation|RInterpToConstant (Transformation|GetActorRotation) (Math|Rotator|MakeRotator :Yaw Yaw) DeltaSeconds 360.0) :bTeleportPhysics false)))''')
parent=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC')
shutil.copy2(root/'Content/Blueprints/SandboxCharacter_CMC.uasset',backup/'SandboxCharacter_CMC.uasset')
for n in B.find_nodes(B.get_graph(parent,'UpdateRotation_PreCMC')):
 for p in B._get_node_info(n).input_pins:
  if p.name=='RotationRate' and '-1.' in p.value:B.set_pin_value(p.pin_id,'0.000000,360.000000,0.000000')
save(parent)
var(bp,'RecoilPitchRemaining','float');var(bp,'RecoilYawRemaining','float')
fn(bp,'UpdateFirearmRecoil',[('DeltaSeconds','float')])
B.compile_blueprint(bp,warnings_as_errors=True);_BlueprintCache.invalidate(bp)
write(bp,'UpdateFirearmRecoil','''(fn UpdateFirearmRecoil (DeltaSeconds)
 (if (Pawn|IsLocallyControlled)
  (bind PitchStep (* (Variables|Default|GetRecoilPitchRemaining) (Math|Float|Clamp(Float) (* DeltaSeconds 18.0) 0.0 1.0)))
  (bind YawStep (* (Variables|Default|GetRecoilYawRemaining) (Math|Float|Clamp(Float) (* DeltaSeconds 18.0) 0.0 1.0)))
  (Pawn|Input|AddControllerPitchInput :Val PitchStep)
  (Pawn|Input|AddControllerYawInput :Val YawStep)
  (Variables|Default|SetRecoilPitchRemaining (- (Variables|Default|GetRecoilPitchRemaining) PitchStep))
  (Variables|Default|SetRecoilYawRemaining (- (Variables|Default|GetRecoilYawRemaining) YawStep))))''')
code=code_from('build_shoulder_camera.py','UpdateShoulderCamera').replace('(and (== (Variables|Default|GetPublicActiveSlot) 2) (== (Variables|Default|GetPublicSidearm) "Weapon.Pistol"))',supported('(CallFunction|GetActiveFirearmID)'))
code=code.replace('(fn UpdateShoulderCamera (DeltaSeconds)','(fn UpdateShoulderCamera (DeltaSeconds)\n (CallFunction|UpdateFirearmRecoil :DeltaSeconds DeltaSeconds)\n (CallFunction|UpdateArmedIdleFacing :DeltaSeconds DeltaSeconds)')
write(bp,'UpdateShoulderCamera',code)
# Preserve authored shot effects while replacing only recoil handling and blend durations.
source=(root/'MigrationStaging/build_firearm_fx.py').read_text()
code=source.split("write(bp,'PlayPistolShot',f'''")[1].split("''')")[0]
code=code.replace('{anim}','(CallFunction|GetShotAnimation)').replace('{fx}','(CallFunction|GetShotFX)').replace('{sound}','(CallFunction|GetShotSound)')
code=code.replace(':BlendInTime 0.02 :BlendOutTime 0.10',':BlendInTime 0.08 :BlendOutTime 0.18')
code=code.replace('(Pawn|Input|AddControllerPitchInput :Val (select','(Variables|Default|SetRecoilPitchRemaining (+ (Variables|Default|GetRecoilPitchRemaining) (select').replace('-1.0 -0.65)))','-1.0 -0.65))))')
code=code.replace('(Pawn|Input|AddControllerYawInput :Val (Math|Random|RandomFloatinRange -0.15 0.15))','(Variables|Default|SetRecoilYawRemaining (+ (Variables|Default|GetRecoilYawRemaining) (Math|Random|RandomFloatinRange -0.15 0.15)))')
write(bp,'PlayPistolShot',code);save(bp)
a=asset('Combat/Animation/Survivor_MM_Rifle_Fire')
a.set_editor_property('ref_pose_type',unreal.AdditiveBasePoseType.ABPT_LOCAL_ANIM_FRAME)
a.set_editor_property('ref_pose_seq',None);a.set_editor_property('ref_frame_index',0)
unreal.EditorAssetLibrary.save_loaded_asset(a,False)
anim=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP')
n=next(n for n in B.find_nodes(B.get_graph(anim,'AnimGraph')) if 'OffsetRoot' in n.get_class().get_name())
O.set_properties(n,'{"node":{"maxRotationError":45,"rotationHalfLife":0.15}}')
save(anim)
print('RECOIL_TURNING_SAVED',backup)



