import unreal,sys,ast,shutil
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
root=Path(unreal.Paths.project_dir());src=root/'Content/AIExample/Combat/Animation/ABP_SurvivorCombat.uasset';dst=root/'Backups/BeforeShoulderCamera-20261117-124627'/src.relative_to(root);dst.parent.mkdir(parents=True,exist_ok=True)
if not dst.exists():shutil.copy2(src,dst)
mesh=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin');assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
bp=asset('Combat/Animation/ABP_SurvivorCombat')
source=ast.parse((root/'MigrationStaging/build_pistol_anim_layer.py').read_text())
code=next(ast.literal_eval(n.args[2]) for n in ast.walk(source) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='write')
code=code.replace('(Math|Float|Clamp(Float) (Math|Rotator|NormalizeAxis Pitch) -70.0 70.0)','(/ (Math|Float|Clamp(Float) (Math|Rotator|NormalizeAxis Pitch) -85.0 85.0) 90.0)')
write(bp,'UpdatePistolLayer',code);save(bp)
