import unreal
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
    p=unreal.GameplayStatics.get_player_pawn(w,0)
    pc=unreal.GameplayStatics.get_player_controller(w,0)
    c=p.get_component_by_class(unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionComponent.BP_InteractionComponent_C'))
    print('PLAYER',p.has_authority(),'POS',p.get_actor_location(),'ROT',pc.get_control_rotation(),'PROMPT',c.get_editor_property('PromptText'))
