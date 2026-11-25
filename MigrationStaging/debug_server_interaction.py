import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionComponent')
t=unreal.AssetExportTask();t.object=bp;t.filename=unreal.Paths.project_saved_dir()+'InteractionValidation/component-current.t3d';t.exporter=unreal.ObjectExporterT3D();t.automated=True;t.prompt=False;unreal.Exporter.run_asset_export_task(t)
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
for w in worlds:
    for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Pawn):
        if p.has_authority() and not p.is_locally_controlled():
            c=p.get_component_by_class(bp.generated_class())
            d=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionTestDoor.BP_InteractionTestDoor_C'))[0]
            print('SERVER',p.get_actor_location(),'REPLICATES',c.get_editor_property('replicates'))
            print('VALID',c.call_method('ValidateTarget',(d,unreal.Vector(-480,0,100.15),unreal.Vector(1,0,0))))
            print('DIRECT_TRY',d.call_method('TryInteract',(p,)))
for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem):
    if 'Transient' in s.get_path_name():
        print('LOCALPLAYER',s.get_outer().get_path_name(),s.get_outer().get_editor_property('PlayerController'))
