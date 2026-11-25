import unreal,json,shutil
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);m=p.get_component_by_class(unreal.SkeletalMeshComponent)
mesh=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin');socket=mesh.find_socket('PistolGrip_R')
root=Path(unreal.Paths.project_dir());backup=root/'Backups/BeforeShoulderCamera-20261117-124627/Content/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin.uasset';backup.parent.mkdir(parents=True,exist_ok=True)
if not backup.exists():shutil.copy2(root/'Content/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin.uasset',backup)
rot=unreal.MathLibrary.inverse_transform_rotation(m.get_socket_transform('hand_r',unreal.RelativeTransformSpace.RTS_WORLD),unreal.Rotator(pitch=0,yaw=p.get_actor_rotation().yaw,roll=0))
print('BEFORE',socket.get_editor_property('relative_rotation'),'AFTER',rot)
socket.set_editor_property('relative_rotation',rot)
assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
