import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out=Path(unreal.Paths.project_saved_dir())/'PistolCombatValidation';out.mkdir(exist_ok=True)
r={}
for path in ['/Game/Blueprints/SandboxCharacter_CMC','/Game/Blueprints/SandboxCharacter_CMC_ABP']:
 b=unreal.load_asset(path);r[path]={'graphs':{g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(b)},'vars':[str(n) for n in B.list_variables(b)]}
(out/'animation-before.json').write_text(json.dumps(r,indent=2))
for name in ['MF_Pistol_Idle_ADS','MM_Pistol_Fire','MM_Pistol_Reload','MM_Pistol_Equip','MM_Pistol_Fire_Montage']:
 a=unreal.load_asset('/Game/Characters/Mannequins/Anims/Pistol/'+name);print('ANIM',name,a.get_class().get_name(),a.get_editor_property('skeleton').get_path_name(),a.get_editor_property('sequence_length'))
print('COMPATIBLE',unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SK_UEFN_Mannequin').get_editor_property('compatible_skeletons'))
