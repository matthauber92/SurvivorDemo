import unreal
print('RESTART',[x for x in dir(unreal.GameModeBase) if 'restart' in x or 'spawn' in x])
