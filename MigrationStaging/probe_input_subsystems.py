import unreal
for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem):
 print(s.get_path_name(),[m for m in dir(s) if 'player' in m or 'continuous' in m])
 print('OUTER',s.get_outer())
print('INJECT',unreal.EnhancedInputLocalPlayerSubsystem.start_continuous_input_injection_for_action.__doc__)
