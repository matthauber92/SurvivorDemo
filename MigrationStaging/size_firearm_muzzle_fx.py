import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
bp=asset('Interaction/BP_SurvivorInteractionCharacter');g=B.get_graph(bp,'PlayPistolShot');changed=0
for n in B.find_nodes(g):
 info=B._get_node_info(n)
 if info.type_id=='Math|Vector|MakeVector':
  coords=[p for p in info.input_pins if p.name in ['X','Y','Z']]
  if len(coords)==3 and all(p.value=='1.800000' or p.value=='1.8' for p in coords):value='0.32'
  elif len(coords)==3 and all(p.value=='1.000000' or p.value=='1.0' for p in coords):value='0.18'
  else:continue
  for p in coords:B.set_pin_value(p.pin_id,value)
  changed+=1
assert changed==2,changed
save(bp)
for name,desc in [('DA_RevolverItem','Six-round revolver. Equip in Sidearm. RMB aim, LMB fire, R reload using Revolver rounds.'),('DA_ShotgunItem','Two-shell shotgun. Equip in Primary or Secondary. Eight pellets per shot, with spread and distance falloff. RMB aim, LMB fire, R reload using Shotgun shells.')]:
 item=asset('Items/'+name);item.set_editor_property('Description',unreal.Text(desc));unreal.EditorAssetLibrary.save_loaded_asset(item,False)
print('MUZZLE_FX_SIZED')
