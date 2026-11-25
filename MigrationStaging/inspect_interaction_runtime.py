import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
for name in ['BPI_Interactable','BP_InteractionTestDoor','BP_InteractionComponent']:
    bp=unreal.load_asset('/Game/AIExample/Interaction/'+name)
    print('ASSET',name)
    for gn in ['GetInteractionPrompt','TryInteract','EventGraph']:
        try: print(gn,B.read_graph_dsl(B.get_graph(bp,gn)))
        except Exception as e: print(str(e))
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
    p=unreal.GameplayStatics.get_player_pawn(w,0)
    door=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionTestDoor.BP_InteractionTestDoor_C'))[0]
    print('DOOR',door.get_path_name(),door.get_editor_property('IsOpen'))
    try: print('PROMPT_DIRECT',door.call_method('GetInteractionPrompt',(p,)))
    except Exception as e: print(str(e))
print('SUBSYSTEM',unreal.get_local_player_subsystem.__doc__)
