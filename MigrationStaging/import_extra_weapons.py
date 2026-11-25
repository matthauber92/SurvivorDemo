import unreal,shutil,datetime,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
assert not unreal.EditorLevelLibrary.get_pie_worlds(False)
backup=root/'Backups'/('AdditionalFirearms-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
for rel in ['AIExample/Items','AIExample/Interaction','AIExample/UI','AIExample/Combat','Characters/UEFN_Mannequin/Meshes']:
 shutil.copytree(root/'Content'/rel,backup/rel)
stage=root/'MigrationStaging/AdditionalWeapons/Stage/Content/AIExample/Weapons/TheHouse'
if not stage.is_dir():
 stage=root.parent/'AIExample-Archive/DirectoryCleanup-20261124/Migrations/AdditionalWeapons/Stage/Content/AIExample/Weapons/TheHouse'
assert stage.is_dir(),stage
count=0
for src in stage.rglob('*.uasset'):
 dst=root/'Content/AIExample/Weapons/TheHouse'/src.relative_to(stage)
 if dst.exists():continue
 dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);count+=1
unreal.AssetRegistryHelpers.get_asset_registry().scan_paths_synchronous(['/Game/AIExample/Weapons/TheHouse'],force_rescan=True)
print('IMPORTED',count,'BACKUP',backup)
for cls,methods in [(unreal.GeometryScript_AssetUtils,['copy_mesh_from_skeletal_mesh','copy_mesh_to_static_mesh']),(unreal.GeometryScript_NewAssetUtils,['create_new_static_mesh_asset_from_mesh'])]:
 for m in methods:print(m,getattr(cls,m).__doc__)
print('OPTIONS',unreal.GeometryScriptCopyMeshFromAssetOptions.__doc__)
print('NEW OPTIONS',unreal.GeometryScriptCreateNewStaticMeshAssetOptions.__doc__)
