import unreal,json
from pathlib import Path
R='/Game/AIExample/Combat/Animation';at=unreal.AssetToolsHelpers.get_asset_tools()
print('FACTORIES',[n for n in dir(unreal) if ('Retarget' in n or 'IKRig' in n) and 'Factory' in n])
source=unreal.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple')
target=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin')
assert source and target
rigs=[]
for name,mesh in [('IK_PistolSource',source),('IK_PistolSurvivor',target)]:
 rig=unreal.load_asset(R+'/'+name)
 if not rig:
  rig=at.create_asset(name,R,unreal.IKRigDefinition,unreal.IKRigDefinitionFactory())
  ctl=unreal.IKRigController.get_controller(rig);assert ctl.set_skeletal_mesh(mesh)
  assert ctl.apply_auto_generated_retarget_definition();assert ctl.apply_auto_fbik()
  unreal.EditorAssetLibrary.save_loaded_asset(rig,only_if_is_dirty=False)
 rigs.append(rig)
retarget=unreal.load_asset(R+'/RTG_PistolSurvivor')
if not retarget:
 retarget=at.create_asset('RTG_PistolSurvivor',R,unreal.IKRetargeter,unreal.IKRetargetFactory())
 ctl=unreal.IKRetargeterController.get_controller(retarget)
 ctl.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE,rigs[0]);ctl.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET,rigs[1])
 ctl.add_default_ops();ctl.auto_map_chains(unreal.AutoMapChainType.FUZZY,True)
 ctl.auto_align_all_bones(unreal.RetargetSourceOrTarget.TARGET)
 unreal.EditorAssetLibrary.save_loaded_asset(retarget,only_if_is_dirty=False)
names=['MF_Pistol_Idle_ADS','MM_Pistol_Fire','MM_Pistol_Reload','MM_Pistol_Equip','MM_Pistol_DryFire','Aim/AO_Pistol']
assets=[unreal.EditorAssetLibrary.find_asset_data('/Game/Characters/Mannequins/Anims/Pistol/'+n) for n in names if not unreal.EditorAssetLibrary.does_asset_exist(R+'/Survivor_'+n.split('/')[-1])]
if assets:
 inputs=unreal.IKRetargetBatchOperationInputs()
 for k,v in {'assets_to_retarget':assets,'source_mesh':source,'target_mesh':target,'ik_retarget_asset':retarget,'prefix':'Survivor_','target_path':R,'use_source_path':False,'include_referenced_assets':True,'overwrite_existing_files':False,'retain_additive_flags':True}.items():inputs.set_editor_property(k,v)
 result=unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
 print('RETARGETED',[str(a.package_name) for a in result])
 unreal.EditorAssetLibrary.save_directory(R,only_if_is_dirty=False,recursive=True)
print('PISTOL_ANIMATIONS_RETARGETED')

