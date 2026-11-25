import unreal,json
from pathlib import Path
for name in ['Revolver','Shotgun']:
 sk=unreal.load_asset('/Game/AIExample/Weapons/TheHouse/04_Weapons/'+name+'/Mesh/SKM_'+name)
 print(name,'SOCKET',sk.find_socket('Muzzle'))
 print('EXPORT',unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh.__doc__)
for n in dir(unreal):
 if 'GeometryScript' in n and any(q in n for q in ['Query','List']):print(n,[m for m in dir(getattr(unreal,n)) if 'vertex' in m or 'array' in m])
