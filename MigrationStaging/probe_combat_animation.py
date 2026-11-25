import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
q={}
for nm in ['MF_Pistol_Idle_ADS','MM_Pistol_Fire','MM_Pistol_Reload','MM_Pistol_Equip','MM_Pistol_Fire_Montage']:
 a=unreal.load_asset('/Game/Characters/Mannequins/Anims/Pistol/'+nm);q[nm]={'class':a.get_class().get_name(),'skeleton':a.get_editor_property('skeleton').get_path_name(),'length':a.get_editor_property('sequence_length')}
print('ANIMS',json.dumps(q))
print('COMPATIBLE',unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SK_UEFN_Mannequin').get_editor_property('compatible_skeletons'))
b=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP');g=B.get_graph(b,'AnimGraph')
print('ANIM_NODES',[(n.get_name(),n.get_class().get_name()) for n in B.find_nodes(g)])
print('ANIM_GRAPHS',[g.get_name() for g in B.list_graphs(b)])
