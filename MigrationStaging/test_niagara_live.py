import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Character) if 'Survivor' in p.get_class().get_name())
print('BEGIN_FX_FULL_SYSTEM_TEST')
fx=unreal.NiagaraFunctionLibrary.spawn_system_at_location(w,unreal.load_asset('/Game/AIExample/Combat/NS_RevolverMuzzle'),p.mesh.get_socket_location('hand_r'),auto_destroy=False,auto_activate=False,pre_cull_check=False)
fx.activate(True)
print('FX',fx.is_active())
