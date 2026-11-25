import unreal,sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
bp=asset('Interaction/BP_SurvivorInteractionCharacter')
source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_pistol_character.py').read_text())
code=next(ast.literal_eval(n.args[2]) for n in ast.walk(source) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='write' and n.args[1].value=='PlayPistolShot')
code=code.replace('(Niagara|SpawnSystemAttached ', '(bind MuzzleFX (Niagara|SpawnSystemAttached ')
code=code.replace(':bAutoDestroy true)', ''':bAutoDestroy true :bAutoActivate false))
  (Transformation|SetRelativeScale3D :self MuzzleFX :NewScale3D "0.18,0.18,0.18")
  (Components|Activation|Activate :self MuzzleFX :bReset true)''')
write(bp,'PlayPistolShot',code);save(bp)
item=asset('Items/DA_PistolItem');item.set_editor_property('Description',unreal.Text('15-round pistol. Equip in Sidearm. Right mouse: aim. Left mouse: fire. R: reload from Handgun Ammo.'));unreal.EditorAssetLibrary.save_loaded_asset(item,only_if_is_dirty=False)
