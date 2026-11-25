import unreal,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from weapon_extension_helpers import *
at=unreal.AssetToolsHelpers.get_asset_tools()
shot=unreal.load_asset(H+'04_Weapons/Shotgun/Mesh/SM_Shotgun')
if not shot:
 sk=unreal.load_asset(H+'04_Weapons/Shotgun/Mesh/SKM_Shotgun');assert sk
 dm,outcome=unreal.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(sk,unreal.DynamicMesh(),unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD())
 assert outcome==unreal.GeometryScriptOutcomePins.SUCCESS
 shot,outcome=unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(dm,H+'04_Weapons/Shotgun/Mesh/SM_Shotgun',unreal.GeometryScriptCreateNewStaticMeshAssetOptions(enable_collision=True))
 assert outcome==unreal.GeometryScriptOutcomePins.SUCCESS
 shot.set_editor_property('static_materials',[unreal.StaticMaterial(material_interface=m.material_interface,material_slot_name=m.material_slot_name) for m in sk.get_editor_property('materials')])
 unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).add_simple_collisions(shot,unreal.ScriptingCollisionShapeType.NDOP26)
 unreal.EditorAssetLibrary.save_loaded_asset(shot,False)
for path in ['04_Weapons/Pistol/Mesh/SM_Pistol','04_Weapons/Revolver/Mesh/SM_Revolver','04_Weapons/Shotgun/Mesh/SM_Shotgun']:
 m=unreal.load_asset(H+path);print('BOUNDS',path,m.get_bounding_box());print('MUZZLE',m.find_socket('Muzzle'))
definition=asset('Items/PDA_ItemDefinition')
specs=[('DA_RevolverItem','Weapon.Revolver','Revolver','Weapon','Sidearm',6,'04_Weapons/Revolver/Mesh/SM_Revolver','04_Weapons/Revolver/Image/IMG_Revolver'),('DA_ShotgunItem','Weapon.Shotgun','Shotgun','Weapon','LongGun',2,'04_Weapons/Shotgun/Mesh/SM_Shotgun','04_Weapons/Shotgun/Image/IMG_Shotgun'),('DA_RevolverAmmo','Ammo.Revolver','Revolver rounds','Ammo','',0,'05_InventoryAssets/Bullets/RevolverBullets/Mesh/SM_Revolver_Ammo','05_InventoryAssets/Bullets/RevolverBullets/Image/IMG_Revolver_Bullets'),('DA_ShotgunAmmo','Ammo.Shotgun','Shotgun shells','Ammo','',0,'05_InventoryAssets/Bullets/ShotgunBullets/Mesh/Shotgun_Bullets','05_InventoryAssets/Bullets/ShotgunBullets/Image/IMG_Shotgun_Bullets')]
items=[]
for name,id,title,category,kind,mag,mesh,icon in specs:
 obj=asset('Items/'+name)
 if not obj:
  f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',definition.generated_class());obj=at.create_asset(name,R+'Items',unreal.DataAsset,f)
 for k,v in {'ItemID':id,'DisplayName':unreal.Text(title),'Description':unreal.Text(title),'Category':category,'MaxStackSize':1 if category=='Weapon' else 60,'EquipmentType':kind,'InitialMagazine':mag,'WorldMesh':unreal.load_asset(H+mesh),'InventoryIcon':unreal.load_asset(H+icon)}.items():obj.set_editor_property(k,v)
 unreal.EditorAssetLibrary.save_loaded_asset(obj,False);items.append(obj)
ammo=asset('Items/DA_HandgunAmmo');ammo.set_editor_property('WorldMesh',unreal.load_asset(H+'05_InventoryAssets/Bullets/PistolBullets/Mesh/SM_Pistol_Ammo'));ammo.set_editor_property('InventoryIcon',unreal.load_asset(H+'05_InventoryAssets/Bullets/PistolBullets/Image/IMG_Pistol_Ammo'));unreal.EditorAssetLibrary.save_loaded_asset(ammo,False)
ui=asset('UI/WBP_Inventory');cdo=unreal.get_default_object(ui.generated_class());catalog=list(cdo.get_editor_property('ItemCatalog'))
for item in items:
 if item not in catalog:catalog.append(item)
cdo.set_editor_property('ItemCatalog',catalog);save(ui)
print('EXTRA_WEAPON_ASSETS_READY')
