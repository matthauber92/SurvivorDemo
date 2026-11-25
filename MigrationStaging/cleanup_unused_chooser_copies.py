import unreal
from pathlib import Path
root=Path(unreal.Paths.project_dir())
for name in ['CHT_PoseSearchDatabases','CHT_PoseSearchDatabases_Dense','CHT_PoseSearchDatabases_Sparse','CHT_PoseSearchDatabases_ExtremeSparse','CHT_CMCCharacterAnimations']:
 path='/Game/AIExample/Combat/Animation/'+name
 assert not (root/'Content'/(path[6:]+'.uasset')).exists(), 'Do not delete a preexisting saved asset'
 if unreal.EditorAssetLibrary.does_asset_exist(path):assert unreal.EditorAssetLibrary.delete_asset(path)
print('Unsaved inspection copies cleaned')
