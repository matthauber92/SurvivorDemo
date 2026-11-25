import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
root='/Game/AIExample/Interaction'
bp=unreal.load_asset(root+'/BP_InteractionComponent')
def fn(name,ins,outs,code):
    g=B.add_function_graph(bp,name)
    existing=[p.name for n in B.find_nodes(g) for p in B._get_node_info(n).output_pins]
    for n,t in ins:
        if n not in existing:
            if t=='Actor':B.add_object_function_param(g,n,unreal.Actor.static_class(),True)
            else:B.add_function_param(g,n,t,True)
    for n,t in outs:
        try:
            if t=='Actor':B.add_object_function_param(g,n,unreal.Actor.static_class(),False)
            else:B.add_function_param(g,n,t,False)
        except Exception:pass
    B.write_graph_dsl(g,code)
    unreal.EditorAssetLibrary.save_loaded_asset(bp)
    print('Compiled',name)
breakhit='(bind (Blocking Initial Time Distance Location ImpactPoint Normal ImpactNormal PhysMat HitActor HitComponent HitBone Bone HitItem Element Face TraceStart TraceEnd) (Collision|BreakHitResult Hit))'
fn('ValidateTarget',[('Target','Actor'),('ViewOrigin','Vector'),('ViewDirection','Vector')],[('Valid','bool')],f'''(fn ValidateTarget (Target ViewOrigin ViewDirection)
 (Utilities|IsValid Target
  (:"Is Valid"
   (bind Pawn (Variables|Default|GetOwnerPawn))
   (bind PawnLocation (Transformation|GetActorLocation :self Pawn))
   (if (and (<= (Math|Vector|VectorLength (- (Transformation|GetActorLocation :self Target) PawnLocation)) (Variables|Default|GetInteractionRange))
            (<= (Math|Vector|VectorLength (- ViewOrigin PawnLocation)) 500.0))
    (bind Direction (Math|Vector|Normalize ViewDirection))
    (bind (Hit DidHit) (Collision|LineTraceByChannel :Start ViewOrigin :End (+ ViewOrigin (* Direction 750.0)) :ActorsToIgnore (Utilities|Array|MakeArray Pawn)))
    {breakhit}
    (if (and DidHit (== HitActor Target))
     (bind (Eyes EyeRotation) (Actor|GetActorEyesViewPoint :self Pawn))
     (bind (SightHit SightBlocked) (Collision|LineTraceByChannel :Start Eyes :End (+ ImpactPoint (* Direction 2.0)) :ActorsToIgnore (Utilities|Array|MakeArray Pawn)))
     (bind (B2 I2 T2 D2 L2 P2 N2 IN2 PM2 SightActor C2 HB2 BN2 HI2 E2 F2 TS2 TE2) (Collision|BreakHitResult SightHit))
     (return (and SightBlocked (== SightActor Target)))
     (else (return false)))
    (else (return false))))
  (:"Is Not Valid" (return false))))''')
fn('UpdateFocus',[],[],f'''(fn UpdateFocus ()
 (Variables|Default|SetFocusedActor "None")
 (Variables|Default|SetPromptText "")
 (bind Pawn (Variables|Default|GetOwnerPawn))
 (if (Pawn|IsLocallyControlled :self Pawn)
  (bind Controller (Pawn|GetController :self Pawn))
  (bind PC (Utilities|Casting|CastToPlayerController :Object Controller)
   (:then
    (bind Camera (Class|PlayerController|GetPlayerCameraManager :self PC))
    (bind Origin (Camera|GetCameraLocation :self Camera))
    (bind Direction (Math|Vector|GetForwardVector (Camera|GetCameraRotation :self Camera)))
    (bind (Hit DidHit) (Collision|LineTraceByChannel :Start Origin :End (+ Origin (* Direction 750.0)) :ActorsToIgnore (Utilities|Array|MakeArray Pawn)))
    {breakhit}
    (if DidHit
     (if (CallFunction|ValidateTarget :Target HitActor :ViewOrigin Origin :ViewDirection Direction)
      (Variables|Default|SetFocusedActor HitActor)
      (bind Prompt (Class|BPIInteractable|GetInteractionPrompt(Message) :self HitActor :Interactor Pawn))
      (Variables|Default|SetPromptText Prompt))))
   (:CastFailed))))''')
fn('RequestInteraction',[],[],'''(fn RequestInteraction ()
 (bind Pawn (Variables|Default|GetOwnerPawn))
 (if (Pawn|IsLocallyControlled :self Pawn)
  (CallFunction|UpdateFocus)
  (Utilities|IsValid (Variables|Default|GetFocusedActor)
   (:"Is Valid"
    (bind PC (Utilities|Casting|CastToPlayerController :Object (Pawn|GetController :self Pawn))
     (:then
      (bind Camera (Class|PlayerController|GetPlayerCameraManager :self PC))
      (CallFunction|ServerInteract :Target (Variables|Default|GetFocusedActor)
       :ViewOrigin (Camera|GetCameraLocation :self Camera)
       :ViewDirection (Math|Vector|GetForwardVector (Camera|GetCameraRotation :self Camera))))
     (:CastFailed)))
   (:"Is Not Valid"))))''')
B.write_graph_dsl(B.get_graph(bp,'EventGraph'),'''(event EventBeginPlay
 (bind Pawn (Utilities|Casting|CastToPawn :Object (Components|GetOwner))
  (:then (Variables|Default|SetOwnerPawn Pawn))
  (:CastFailed)))
(event EventTick (DeltaSeconds)
 (Utilities|IsValid (Variables|Default|GetOwnerPawn)
  (:"Is Valid" (CallFunction|UpdateFocus))
  (:"Is Not Valid")))
(event Custom|ServerInteract (Target ViewOrigin ViewDirection)
 (if (Networking|HasAuthority :self (Components|GetOwner))
  (if (CallFunction|ValidateTarget :Target Target :ViewOrigin ViewOrigin :ViewDirection ViewDirection)
   (Class|BPIInteractable|TryInteract(Message) :self Target :Interactor (Variables|Default|GetOwnerPawn)))))''')
unreal.EditorAssetLibrary.save_loaded_asset(bp)
print('Component complete')
