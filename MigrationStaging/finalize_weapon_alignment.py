import unreal,ast,toolset_registry
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter')
src=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_weapon_switching.py').read_text())
with toolset_registry.tool_raising_exceptions():
 for x in ast.walk(src):
  if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='write' and isinstance(x.args[1],ast.Constant) and x.args[1].value=='UpdateWeaponVisual':
   B.write_graph_dsl(B.get_graph(bp,'UpdateWeaponVisual'),ast.literal_eval(x.args[2]))
 B.compile_blueprint(bp,warnings_as_errors=True);assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)

