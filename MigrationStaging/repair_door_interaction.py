import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionTestDoor')
iface=unreal.load_asset('/Game/AIExample/Interaction/BPI_Interactable')
print('IMPLEMENTS',unreal.SystemLibrary.does_implement_interface(unreal.get_default_object(bp.generated_class()),iface.generated_class()))
print('OBJECT_APIS',[n for n in dir(unreal) if 'Blueprint' in n and ('Library' in n or 'Utils' in n)])
print('ONREP',B.read_graph_dsl(B.get_graph(bp,'OnRep_IsOpen')))
print('INPUT', [n for n in dir(unreal.EnhancedInputLibrary) if 'subsystem' in n or 'player' in n])
for name,out,typ in [('GetInteractionPrompt','Prompt','text'),('TryInteract','Accepted','bool')]:
    g=B.get_graph(bp,name)
    B.add_object_function_param(g,'Interactor',unreal.Pawn.static_class(),True)
    B.add_function_param(g,out,typ,False)
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
unreal.SystemLibrary.execute_console_command(world,'set '+bp.get_path_name()+' ImplementedInterfaces ((Interface="'+iface.generated_class().get_path_name()+'"))')
B.compile_blueprint(bp)
print('IMPLEMENTS_AFTER',unreal.SystemLibrary.does_implement_interface(unreal.get_default_object(bp.generated_class()),iface.generated_class()))
exec(open(unreal.Paths.project_dir()+'MigrationStaging/build_interaction_logic.py').read())
