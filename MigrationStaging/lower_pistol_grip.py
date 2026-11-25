import unreal,shutil,datetime
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0]
p=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Character) if 'Survivor' in p.get_class().get_name())
mesh=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin');socket=mesh.find_socket('PistolGrip_R');gun=p.get_editor_property('SidearmVisual')
root=Path(unreal.Paths.project_dir());backup=root/'Backups'/('PistolGripPreview-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir(parents=True)
shutil.copy2(root/'Content/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin.uasset',backup/'SKM_UEFN_Mannequin.uasset')
before=socket.get_editor_property('relative_location')
after=unreal.MathLibrary.inverse_transform_location(p.mesh.get_socket_transform('hand_r',unreal.RelativeTransformSpace.RTS_WORLD),gun.get_world_location()+unreal.Vector(0,0,-4.5))
socket.set_editor_property('relative_location',after)
assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
print('GRIP_LOCATION',before,after)
