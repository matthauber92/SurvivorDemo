import unreal,toolset_registry,shutil
from pathlib import Path
from datetime import datetime
from editor_toolset.toolsets.blueprint import BlueprintTools as B
root=Path(unreal.Paths.project_dir())
backup=root/'Backups'/('BeforeHipClearance-'+datetime.now().strftime('%Y%m%d-%H%M%S'))
backup.mkdir(parents=True,exist_ok=True)
shutil.copy2(root/'Content/AIExample/Interaction/BP_SurvivorInteractionCharacter.uasset',backup)
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter')
g=B.get_graph(bp,'UpdateWeaponVisual')
with toolset_registry.tool_raising_exceptions():
 matches=[]
 for node in B.find_nodes(g):
  info=B._get_node_info(node)
  if 'MakeTransform' not in info.type_id:continue
  for pin in info.input_pins:
   if pin.name=='Location' and B.get_pin_value(pin.pin_id).replace(' ','')=='-5,-2,18':matches.append(pin.pin_id)
 assert matches,'Expected a hip transform'
 for pin in matches:B.set_pin_value(pin,'-5,-2,21')
 B.compile_blueprint(bp,warnings_as_errors=True)
 assert bp.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE
 assert all(B.get_pin_value(pin).replace(' ','')=='-5,-2,21' for pin in matches)
 assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 print('HIP_CLEARANCE_SAVED: 3 cm farther outward; only hip location changed.')

