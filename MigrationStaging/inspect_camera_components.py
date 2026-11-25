import unreal,json
from pathlib import Path
from editor_toolset.toolsets.actor import ActorTools as A
from editor_toolset.toolsets.blueprint import BlueprintTools as B
print('ACTOR_API', [n for n in dir(A) if 'component' in n.lower()])
bp=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC')
print('PARENT',B.get_parent(bp))
print('COMPONENTS',A.get_components(B.get_default_object(bp)))
print('CAMERAS', [a.object_path if hasattr(a,'object_path') else str(a.package_name) for a in unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path('/Game',True) if 'camera' in str(a.package_name).lower()])
print('DSLPC',B.read_graph_dsl(B.get_graph(unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController'),'EventGraph')))
