import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from weapon_extension_helpers import *
from editor_toolset.toolsets.skeletal_mesh import SkeletalMeshTools as S
mesh=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin');pistol=mesh.find_socket('PistolGrip_R')
rot=pistol.get_editor_property('relative_rotation');loc=pistol.get_editor_property('relative_location')
specs=[('RevolverGrip_R','hand_r',loc+unreal.MathLibrary.quat_rotate_vector(rot.quaternion(),unreal.Vector(3,0,1)),rot),('RevolverHolster','pelvis',unreal.Vector(-5,-2,19.5),unreal.Rotator(pitch=0,yaw=170,roll=-90)),('ShotgunGrip_R','hand_r',loc+unreal.MathLibrary.quat_rotate_vector(rot.quaternion(),unreal.Vector(14,0,1)),unreal.MathLibrary.compose_rotators(unreal.Rotator(yaw=90),rot)),('ShotgunPrimaryHolster','spine_03',unreal.Vector(10,-18,-12),unreal.Rotator(yaw=90)),('ShotgunSecondaryHolster','spine_03',unreal.Vector(10,-18,12),unreal.Rotator(yaw=90))]
for name,bone,location,rotation in specs:
 if mesh.find_socket(name):continue
 s=S.add_socket(mesh,name,bone);s.set_editor_property('relative_location',location);s.set_editor_property('relative_rotation',rotation)
unreal.EditorAssetLibrary.save_loaded_asset(mesh,False)
for name,location,rotation in [('Revolver',unreal.Vector(16.6,0,1.25),unreal.Rotator()),('Shotgun',unreal.Vector(0,-56.4,1.4),unreal.Rotator(yaw=-90))]:
 m=unreal.load_asset(H+'04_Weapons/'+name+'/Mesh/SM_'+name)
 if not m.find_socket('Muzzle'):
  s=unreal.new_object(unreal.StaticMeshSocket,outer=m);s.set_editor_property('socket_name','Muzzle');s.set_editor_property('relative_location',location);s.set_editor_property('relative_rotation',rotation);m.add_socket(s)
 unreal.EditorAssetLibrary.save_loaded_asset(m,False)
bp=asset('Interaction/BP_SurvivorInteractionCharacter')
write(bp,'UpdateWeaponVisual','''(fn UpdateWeaponVisual (Slot ID Visual)
 (Development|SetHiddeninGame :self Visual :NewHidden true)
 (if (or (or (== ID "Weapon.Pistol") (== ID "Weapon.Revolver")) (or (== ID "Weapon.Shotgun") (== ID "Weapon.TestLongGun")))
  (if (== ID "Weapon.Pistol") (Components|StaticMesh|SetStaticMesh :self Visual :NewMesh "/Game/AIExample/Weapons/TheHouse/04_Weapons/Pistol/Mesh/SM_Pistol.SM_Pistol"))
  (if (== ID "Weapon.Revolver") (Components|StaticMesh|SetStaticMesh :self Visual :NewMesh "/Game/AIExample/Weapons/TheHouse/04_Weapons/Revolver/Mesh/SM_Revolver.SM_Revolver"))
  (if (== ID "Weapon.Shotgun") (Components|StaticMesh|SetStaticMesh :self Visual :NewMesh "/Game/AIExample/Weapons/TheHouse/04_Weapons/Shotgun/Mesh/SM_Shotgun.SM_Shotgun"))
  (if (== ID "Weapon.TestLongGun") (Components|StaticMesh|SetStaticMesh :self Visual :NewMesh "/Engine/BasicShapes/Cube.Cube"))
  (Variables|Default|SetAttachSocket (select (== Slot 1) "SecondaryHolster" "PrimaryHolster"))
  (if (== ID "Weapon.Pistol") (Variables|Default|SetAttachSocket "PistolHolster"))
  (if (== ID "Weapon.Revolver") (Variables|Default|SetAttachSocket "RevolverHolster"))
  (if (== ID "Weapon.Shotgun") (Variables|Default|SetAttachSocket (select (== Slot 1) "ShotgunSecondaryHolster" "ShotgunPrimaryHolster")))
  (if (== Slot (Variables|Default|GetPublicActiveSlot))
   (Variables|Default|SetAttachSocket "LongGunGrip_R")
   (if (== ID "Weapon.Pistol") (Variables|Default|SetAttachSocket "PistolGrip_R"))
   (if (== ID "Weapon.Revolver") (Variables|Default|SetAttachSocket "RevolverGrip_R"))
   (if (== ID "Weapon.Shotgun") (Variables|Default|SetAttachSocket "ShotgunGrip_R")))
  (Transformation|AttachComponentToComponent :self Visual :Parent (Variables|Character|GetMesh) :SocketName (Variables|Default|GetAttachSocket) :LocationRule "SnapToTarget" :RotationRule "SnapToTarget" :ScaleRule "SnapToTarget" :bWeldSimulatedBodies false)
  (Transformation|SetRelativeScale3D :self Visual :NewScale3D (select (== ID "Weapon.TestLongGun") (Math|Vector|MakeVector 0.65 0.07 0.12) (Math|Vector|MakeVector 1.0 1.0 1.0)))
  (Development|SetHiddeninGame :self Visual :NewHidden false)))''')
save(bp)
