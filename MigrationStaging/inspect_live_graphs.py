import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
for name,gn in [('BP_InteractionTestDoor','OnRep_IsOpen'),('BP_InteractionTestDoor','GetInteractionPrompt'),('BP_SurvivorInteractionCharacter','EventGraph')]:
    bp=unreal.load_asset('/Game/AIExample/Interaction/'+name)
    print(name,gn,B.read_graph_dsl(B.get_graph(bp,gn)))
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
    p=unreal.GameplayStatics.get_player_pawn(w,0)
    c=p.get_component_by_class(unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionComponent.BP_InteractionComponent_C'))
    print('PROMPT',p.has_authority(),c.get_editor_property('PromptText'))
    d=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionTestDoor.BP_InteractionTestDoor_C'))[0]
    d.call_method('OnRep_IsOpen')
    print('HINGE',d.get_editor_property('DoorHinge').get_editor_property('relative_rotation'))
