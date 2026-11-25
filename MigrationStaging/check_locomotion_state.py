import unreal,json
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);a=p.get_component_by_class(unreal.SkeletalMeshComponent).get_anim_instance()
print({n:str(a.get_editor_property(n)) for n in ['MovementMode','MovementState','Speed2D','CurrentSelectedAnim','CurrentSelectedDatabase','ValidDatabases']})
