from pathlib import Path
import sys
import unreal as u

project = Path(u.Paths.convert_relative_path_to_full(u.Paths.project_dir()))
sys.path[:0] = [str(project / 'Tools/Unreal'), str(project / 'MigrationStaging')]
from combat_helpers import B, asset, fn, pin, save, toolset_registry, var, write
from camera_graph import prune_camera_graph

def active_nodes(g):
    nodes=B.find_nodes(g)
    stack=[next(n for n in nodes if isinstance(n,u.K2Node_FunctionEntry))]
    seen=set()
    while stack:
        n=stack.pop()
        if n in seen:continue
        seen.add(n)
        for q in B._get_node_info(n).output_pins:
            if q.name.lower() in ('then','else','is valid','is not valid','castfailed'):stack.extend(x.node for x in q.connected_pins)
    return seen

s=asset('Interaction/BP_SurvivorInteractionCharacter')
for n,t in [('AnkleCameraOwned','bool'),('AnkleCameraMix','float'),('AnkleCameraAge','float'),('AnkleCameraEntryArm','float'),('AnkleCameraEntryFOV','float'),('AnkleCameraEntrySocket','Vector'),('AnkleCameraEntryPivot','Vector'),('AnkleCameraEntryRotation','rotator'),('AnkleCameraEntryLens','rotator'),('AnkleCameraEntryUsesControl','bool')]:var(s,n,t)
fn(s,'FrameAnkleBite',[('DeltaSeconds','float')])
B.compile_blueprint(s)
def G(n):return '(Variables|Default|GetAnkleCamera'+n+')'
def S(n,val):return '(Variables|Default|SetAnkleCamera'+n+' '+val+')'
def smooth(x):return f'(* (* {x} {x}) (- 3.0 (* 2.0 {x})))'
clip='/Game/Survivor/Zombies/Animations/Survivor_AnkleBite_KickFree.Survivor_AnkleBite_KickFree'
cam='(Variables|Default|GetShoulderCamera)'
def pulse(center,width):
    x=f'(Math|Float|Clamp(Float) (- 1.0 (/ (Math|Float|Absolute(Float) (- {G("Age")} {center})) {width})) 0.0 1.0)'
    return smooth(x)
body=f"""(fn FrameAnkleBite (DeltaSeconds)
 (bind Bm (Variables|Default|GetShoulderBoom))
 (bind Anim (Components|SkeletalMesh|GetAnimInstance :self (Variables|Character|GetMesh)))
 (bind Active (Animation|Montage|IsPlayingSlotAnimation :self Anim :Asset "{clip}" :SlotNodeName "SurvivorBiteReaction"))
 (if (and (not Active) (not {G('Owned')})) (return))
 (if Active
   {S('Age','(Animation|Montage|MontageGetPosition :self Anim :Montage (Animation|Montage|GetCurrentActiveMontage :self Anim))')}
   (else {S('Mix',f'(Math|Float|Max(Float) 0.0 (- {G("Mix")} (* DeltaSeconds 2.8)))')}))
 (if (or (>= {G('Age')} 4.16) (and (not Active) (<= {G('Mix')} 0.0)))
   (if {G('Owned')}
    (Class|SpringArmComponent|SetUsePawnControlRotation {G('EntryUsesControl')} Bm)
    (Transformation|SetRelativeRotation :self Bm :NewRotation {G('EntryRotation')})
    (Transformation|SetRelativeRotation :self {cam} :NewRotation {G('EntryLens')})
    (Class|SpringArmComponent|SetTargetOffset {G('EntryPivot')} Bm)
    {S('Owned','false')})
   (return))
 (if (not {G('Owned')})
  {S('EntryUsesControl','(Class|SpringArmComponent|GetUsePawnControlRotation Bm)')}
  {S('EntryRotation','(Class|SceneComponent|GetRelativeRotation Bm)')}
  {S('EntrySocket','(Class|SpringArmComponent|GetSocketOffset Bm)')}
  {S('EntryLens',f'(Class|SceneComponent|GetRelativeRotation {cam})')}
  {S('EntryPivot','(Class|SpringArmComponent|GetTargetOffset Bm)')}
  {S('Owned','true')})
 (bind In (Math|Float|Clamp(Float) (/ {G('Age')} .74) 0.0 1.0))
 (bind Out (Math|Float|Clamp(Float) (/ (- {G('Age')} 3.43) .73) 0.0 1.0))
 (if Active {S('Mix',f'(* {smooth("In")} (- 1.0 {smooth("Out")}))')})
 (bind Alpha {G('Mix')})
 (bind View (Pawn|GetControlRotation :self (Pawn|GetController)))
 (bind (VR VP VY) (Math|Rotator|BreakRotator View))
 (bind Bite (- (* 1.65 {pulse(.96,.06)}) (* .72 {pulse(1.04,.09)})))
 (bind Impact (+ (- (* 6.4 {pulse(2.72,.057)}) (* 4.35 {pulse(2.79,.064)})) (- (* 2.35 {pulse(2.865,.069)}) (* .95 {pulse(2.95,.085)}))))
 (bind Shake (* Alpha (+ Bite Impact)))
 (bind Orbit (Math|Rotator|MakeRotator :Yaw (- VY 32.0) :Pitch -71.0))
 (Class|SpringArmComponent|SetUsePawnControlRotation false Bm)
 (Transformation|SetWorldRotation :self Bm :NewRotation (Math|Rotator|Lerp(Rotator) View Orbit Alpha true))
 (bind (LR LP LY) (Math|Rotator|BreakRotator {G('EntryLens')}))
 (Transformation|SetRelativeRotation :self {cam} :NewRotation (Math|Rotator|MakeRotator :Pitch (+ LP Shake) :Yaw (+ LY (* -.67 Shake)) :Roll (+ LR (* .92 Shake))))
 (bind Focus (+ (* (Transformation|GetActorForwardVector) 56.0) (Math|Vector|MakeVector :Z -22.0)))
 (Class|SpringArmComponent|SetTargetOffset (Math|Vector|Lerp(Vector) {G('EntryPivot')} (+ {G('EntryPivot')} Focus) Alpha) Bm)
 (bind Shoulder (Math|Vector|MakeVector :Y (+ 12.0 (* 1.05 Shake))))
 (Class|SpringArmComponent|SetSocketOffset (Math|Vector|Lerp(Vector) {G('EntrySocket')} Shoulder Alpha) Bm))"""
write(s,'FrameAnkleBite',body)
prune_camera_graph(B.get_graph(s,'FrameAnkleBite'))
with toolset_registry.tool_raising_exceptions():
 g=B.get_graph(s,'UpdateShoulderCamera');active=active_nodes(g)
 if not any('frameanklebite' in B._get_node_info(n).type_id.lower() for n in active):
    last=next(n for n in active if B._get_node_info(n).type_id.lower()=='camera|setfieldofview')
    assert not next(q for q in B._get_node_info(last).output_pins if q.name=='then').connected_pins
    entry=next(n for n in active if isinstance(n,u.K2Node_FunctionEntry))
    call=B.create_node(g,'CallFunction|FrameAnkleBite',u.IntPoint(1880,420))
    B.connect_pins(pin(last,'then',True),pin(call,'execute'))
    B.connect_pins(pin(entry,'DeltaSeconds',True),pin(call,'DeltaSeconds'))
 save(s)
print('ESCAPE_CAMERA_FINAL_READY')



