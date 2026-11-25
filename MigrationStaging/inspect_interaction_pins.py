import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionComponent')
g=B.get_graph(bp,'EventGraph')
terms=['GetCameraLocation','GetCameraRotation','GetForwardVector','VectorDistance','BreakHitResult','GetActorLocation','GetGameTime','ImplementsInterface','IsValid','GetPlayerViewPoint','GetOwner','GetComponentByClass','HasAuthority','GetWorldDelta','SetRelativeRotation','TryInteract','GetInteractionPrompt']
types=[]
for term in terms:types+=list(B.find_node_types(g,term,[]))
types += ['Collision|LineTraceByChannel','Class|PlayerController|GetPlayerCameraManager','Actor|GetActorEyesViewPoint']
data={}
for t in dict.fromkeys(types):
    try:data[t]=str(B.get_node_type_pins(g,t))
    except Exception as e:data[t]=str(e)
(Path(unreal.Paths.project_saved_dir())/'InteractionValidation/pins.json').write_text(json.dumps(data,indent=2))
