import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionHUD')
g=B.get_graph(bp,'EventGraph')
for term in ['DrawHUD','DrawText','GetOwningPawn','GetPromptText','ToString(Text)']:
    print(term,list(B.find_node_types(g,term,[])))
print('PARENT',unreal.get_default_object(bp.generated_class()).get_class())
B.write_graph_dsl(g,'''(event AddEvent|EventReceiveDrawHUD (SizeX SizeY)
 (bind Pawn (HUD|GetOwningPawn))
 (Utilities|IsValid Pawn
  (:"Is Valid"
   (bind Component (Utilities|Casting|CastToBP_InteractionComponent :Object
     (Actor|GetComponentbyClass :self Pawn :ComponentClass "/Game/AIExample/Interaction/BP_InteractionComponent.BP_InteractionComponent_C"))
    (:then
     (HUD|DrawText
      :Text (Utilities|String|ToString(Text) (Class|BPInteractionComponent|GetPromptText :self Component))
      :TextColor "(R=1,G=1,B=1,A=1)" :ScreenX (- (* SizeX 0.5) 100.0) :ScreenY (* SizeY 0.7) :Scale 1.3))
    (:CastFailed)))
  (:"Is Not Valid")))''')
print('RESULT',B.read_graph_dsl(g))
unreal.EditorAssetLibrary.save_loaded_asset(bp)
