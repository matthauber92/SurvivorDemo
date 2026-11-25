import unreal,json
from pathlib import Path
R='/Game/AIExample/';report={}
for name in ['DA_RevolverItem','DA_ShotgunItem','DA_RevolverAmmo','DA_ShotgunAmmo','DA_HandgunAmmo']:
 a=unreal.load_asset(R+'Items/'+name);m=a.get_editor_property('WorldMesh');report[name]={'mesh':m.get_path_name(),'icon':a.get_editor_property('InventoryIcon').get_path_name(),'materials':[m.get_material(i).get_path_name() if m.get_material(i) else None for i in range(m.get_num_sections(0))]};assert all(report[name]['materials'])
mesh=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin')
from editor_toolset.toolsets.object import ObjectTools as O
print('PREVIEW_PROPS',[k for k in json.loads(O.list_properties(mesh)) if 'preview' in k.lower()])
for n in ['RevolverGrip_R','ShotgunGrip_R']:
 s=mesh.find_socket(n);report[n]={'location':str(s.relative_location),'rotation':str(s.relative_rotation)}
report['active_anim']=unreal.get_default_object(unreal.load_asset(R+'Interaction/BP_SurvivorInteractionCharacter').generated_class()).mesh.get_editor_property('anim_class').get_path_name()
(Path(unreal.Paths.project_saved_dir())/'firearm-asset-validation.json').write_text(json.dumps(report,indent=2))
ed=unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
ed.close_all_editors_for_asset(unreal.load_asset(R+'Weapons/TheHouse/07_ParticleFX/Pistol/NS_Pistol'))
print('WEAPON_ASSETS_VALIDATED')
