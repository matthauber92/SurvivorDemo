import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
root='/Game/AIExample/Interaction'
door=unreal.load_asset(root+'/BP_InteractionTestDoor')
comp=unreal.load_asset(root+'/BP_InteractionComponent')
def write(bp,name,code):
    g=B.get_graph(bp,name)
    B.write_graph_dsl(g,code)
    unreal.EditorAssetLibrary.save_loaded_asset(bp)
    print('Compiled',bp.get_name(),name)
write(door,'OnRep_IsOpen','''(fn OnRep_IsOpen ()
  (Transformation|SetRelativeRotation :self (Variables|Default|GetDoorHinge)
    :NewRotation (Math|Rotator|MakeRotator :Yaw (select (Variables|Default|GetIsOpen) 90.0 0.0))))''')
write(door,'GetInteractionPrompt','''(fn GetInteractionPrompt (Interactor)
  (return (select (Variables|Default|GetIsOpen) "Press E to Close Door" "Press E to Open Door")))''')
write(door,'TryInteract','''(fn TryInteract (Interactor)
  (if (Networking|HasAuthority)
    (if (>= (Utilities|Time|GetGameTimeinSeconds) (Variables|Default|GetNextInteractionTime))
      (if (<= (Math|Vector|VectorLength (- (Transformation|GetActorLocation :self Interactor) (Transformation|GetActorLocation))) 250.0)
        (Variables|Default|SetNextInteractionTime (+ (Utilities|Time|GetGameTimeinSeconds) 0.5))
        (Variables|Default|SetIsOpen (not (Variables|Default|GetIsOpen)))
        (return true)
        (else (return false)))
      (else (return false)))
    (else (return false))))''')
print('RPC',B.read_graph_dsl(B.get_graph(comp,'EventGraph')))
data={}
g=B.get_graph(comp,'EventGraph')
for term in ['MakeArray','Normalize','DotProduct','TextToString','ToString','InputAction','SetActorTick','GetOwnerPawn']:
    data[term]=list(B.find_node_types(g,term,[]))
(Path(unreal.Paths.project_saved_dir())/'InteractionValidation/logic-types.json').write_text(json.dumps(data,indent=2))

