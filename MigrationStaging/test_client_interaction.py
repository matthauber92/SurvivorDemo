import unreal
wc=unreal.EditorLevelLibrary.get_pie_worlds(False)
comp_class=unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionComponent.BP_InteractionComponent_C')
door_class=unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionTestDoor.BP_InteractionTestDoor_C')
for w in wc:
    p=unreal.GameplayStatics.get_player_pawn(w,0)
    c=p.get_component_by_class(comp_class)
    door=unreal.GameplayStatics.get_all_actors_of_class(w,door_class)[0]
    print('STATE',p.has_authority(),str(c.get_editor_property('PromptText')),door.get_editor_property('IsOpen'))
    if not p.has_authority():
        c.call_method('RequestInteraction')
        print('REQUESTED_CLIENT')
print('SUBSYSTEM_LOOKUP',[n for n in dir(unreal) if 'Subsystem' in n and 'Library' in n])
print('ITERATOR',hasattr(unreal,'ObjectIterator'))
