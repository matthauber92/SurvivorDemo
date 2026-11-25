import unreal
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
print('EDITOR_WORLD',str(world))
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.LevelEditorPlaySettings'))
for prop in ['PlayNetMode','PlayNumberOfClients','RunUnderOneProcess']:
    try: print(prop,settings.get_editor_property(prop))
    except Exception as e: print(str(e))
print('WORLD_APIS',[n for n in dir(unreal.EditorLevelLibrary) if 'world' in n])
print('INPUT_APIS',[n for n in dir(unreal.EnhancedInputLocalPlayerSubsystem) if 'inject' in n or 'mapping' in n])
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
for w in worlds:
    print('WORLD',w.get_path_name())
    pc=unreal.GameplayStatics.get_player_controller(w,0)
    pawn=unreal.GameplayStatics.get_player_pawn(w,0)
    print('PLAYER',pc,pawn)
    if pawn:
        comp=pawn.get_component_by_class(unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionComponent.BP_InteractionComponent_C'))
        print('PAWN',pawn.get_actor_location(),'COMP',comp)
        for p in ['OwnerPawn','FocusedActor','PromptText','InputReady']:
            print(p,comp.get_editor_property(p))
        print('CAMERA',pc.player_camera_manager.get_camera_location(),pc.player_camera_manager.get_camera_rotation(),'HUD',pc.get_hud())
        print('CALL',comp.call_method('UpdateFocus'))

