import unreal,json
from editor_toolset.toolsets.object import ObjectTools as O
for p in ['/Niagara/VectorFields/Assets/TilingCurl32','/Game/AIExample/Combat/NS_RevolverMuzzle']:
 o=unreal.load_asset(p);print(p,O.list_properties(o))
