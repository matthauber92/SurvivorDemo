import unreal
action=unreal.load_asset('/Game/AIExample/Interaction/IA_SurvivorInteract')
for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem):
    if 'Transient' in s.get_path_name():
        s.inject_input_vector_for_action(action,unreal.Vector(1,0,0),[],[])
        print('INJECTED',s.get_path_name())
