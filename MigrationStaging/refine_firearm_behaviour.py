import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from weapon_extension_helpers import *
from editor_toolset.toolsets.blueprint import _BlueprintCache
bp=asset('Interaction/BP_SurvivorInteractionCharacter')
fn(bp,'GetEquipAnimation',[],[('Asset',unreal.AnimSequenceBase.static_class())])
write(bp,'GetEquipAnimation','''(fn GetEquipAnimation ()
 (if (== (CallFunction|GetActiveFirearmID) "Weapon.Shotgun") (return "/Game/AIExample/Combat/Animation/Survivor_MM_Rifle_Equip.Survivor_MM_Rifle_Equip"))
 (return "/Game/AIExample/Combat/Animation/Survivor_MM_Pistol_Equip.Survivor_MM_Pistol_Equip"))''')
var(bp,'BarrelBlocked','bool');B.compile_blueprint(bp,warnings_as_errors=True);_BlueprintCache.invalidate(bp)
code=code_from('build_pistol_character.py','CheckPistolEquip').replace('(and (== (Variables|Default|GetPublicActiveSlot) 2) (== (Variables|Default|GetPublicSidearm) "Weapon.Pistol"))',supported('(CallFunction|GetActiveFirearmID)')).replace('"/Game/AIExample/Combat/Animation/Survivor_MM_Pistol_Equip.Survivor_MM_Pistol_Equip"','(CallFunction|GetEquipAnimation)');write(bp,'CheckPistolEquip',code)
code=code_from('extend_firearm_character.py','PerformPistolShot')
code=code.replace('(Math|Vector|MakeRotfromX','(Math|Rotator|MakeRotfromX').replace('Cos(degrees)','Cos(Degrees)').replace('Sin(degrees)','Sin(Degrees)')
code=code.replace('(bind Angle (* i (/ 360.0 (Variables|Default|GetShotgunPelletCount))))','(bind Angle (* (- i 1) (/ 360.0 (Math|Integer|Max(Integer) 1 (- (Variables|Default|GetShotgunPelletCount) 1)))))')
insert='''  (bind Eye (+ (Transformation|GetActorLocation) (Math|Vector|MakeVector 0.0 0.0 50.0)))
  (bind (BarrelHit Blocked) (Collision|LineTraceByChannel :Start Eye :End (Variables|Default|GetShotStart) :TraceChannel "TraceTypeQuery1" :ActorsToIgnore (Variables|Default|GetShotIgnoreActors)))
  (Variables|Default|SetBarrelBlocked Blocked)
  (if Blocked
   (bind (BB BI BT BD BL BarrelImpact BN BIN BPM BA BC BHB BBn BItem BE BF BS BEnd) (Collision|BreakHitResult BarrelHit))
   (Variables|Default|SetShotAimPoint BarrelImpact)
   (Variables|Default|SetShotStart Eye))
'''
code=code.replace('  (Variables|Default|SetShotDirection',insert+'  (Variables|Default|SetShotDirection',1)
code=code.replace('(if (== (CallFunction|GetActiveFirearmID) "Weapon.Shotgun")\n   (bind AimRot','(if (and (== (CallFunction|GetActiveFirearmID) "Weapon.Shotgun") (not (Variables|Default|GetBarrelBlocked)))\n   (bind AimRot')
write(bp,'PerformPistolShot',code);save(bp)
print('REFRESH_AIM',B.read_graph_dsl(B.get_graph(bp,'RefreshPistolAim')))
