import unreal,json
from editor_toolset.toolsets.object import ObjectTools as O
R='/Game/AIExample/Combat/'
src=unreal.load_asset('/Niagara/VectorFields/Assets/TilingCurl32');print('SOURCE',O.get_properties(src,['bAllowCPUAccess','sizeX','sizeY','sizeZ']))
vf=unreal.load_asset(R+'VF_WeaponSmoke') or unreal.EditorAssetLibrary.duplicate_asset(src.get_path_name(),R+'VF_WeaponSmoke')
assert O.set_properties(vf,json.dumps({'bAllowCPUAccess':True}));unreal.EditorAssetLibrary.save_loaded_asset(vf,False)
for path in ['/Game/AIExample/Weapons/TheHouse/07_ParticleFX/Pistol/NS_Pistol',R+'NS_RevolverMuzzle',R+'NS_ShotgunMuzzle',R+'NS_BulletImpact']:
 system=unreal.load_asset(path);count=0
 for o in unreal.ObjectIterator(unreal.NiagaraDataInterface):
  if o.get_path_name().startswith(path+'.') and 'VectorField' in o.get_class().get_name():o.set_editor_property('field',vf);count+=1
 unreal.EditorAssetLibrary.save_loaded_asset(system,False);print('FIXED_FIELD',path,count)
mesh=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin');edit=unreal.get_editor_subsystem(unreal.AssetEditorSubsystem);edit.close_all_editors_for_asset(mesh);edit.open_editor_for_assets([mesh])
