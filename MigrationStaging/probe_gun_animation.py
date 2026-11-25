import unreal
from editor_toolset.toolsets.skeletal_mesh import SkeletalMeshTools as S
mesh=unreal.load_asset('/Game/AIExample/Weapons/TheHouse/04_Weapons/Pistol/Mesh/SKM_Pistol')
print('GUN_BONES',S.get_bone_names(mesh));print('ANIM_FACTORY',unreal.AnimSequenceFactory.__doc__)
print('CONTROLLER',[x for x in dir(unreal.AnimSequence) if 'controller' in x or 'data_model' in x])
print('ADCTRL',[x for x in dir(unreal.AnimationDataController) if any(t in x for t in ['bone','frame','initialize'])])
for m in ['set_bone_track_keys','add_bone_curve','set_number_of_frames']:print(m,getattr(unreal.AnimationDataController,m).__doc__ if hasattr(unreal.AnimationDataController,m) else '')
