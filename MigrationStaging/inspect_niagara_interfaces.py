import unreal
for n in dir(unreal):
 if 'NiagaraDataInterfaceVectorField'==n:print(getattr(unreal,n).__doc__)
for system in ['/Game/AIExample/Weapons/TheHouse/07_ParticleFX/Pistol/NS_Pistol','/Game/AIExample/Combat/NS_RevolverMuzzle','/Game/AIExample/Combat/NS_ShotgunMuzzle','/Game/AIExample/Combat/NS_BulletImpact']:
 asset=unreal.load_asset(system)
 print('SYSTEM',system)
 for o in unreal.ObjectIterator(unreal.NiagaraDataInterface):
  if o.get_path_name().startswith(system+'.'):
   print('DI',o.get_class().get_name(),o.get_path_name());
   if 'VectorField' in o.get_class().get_name():print('FIELD',o.get_editor_property('field'))
