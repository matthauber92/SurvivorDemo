import unreal
R='/Game/AIExample/Combat/Animation';source=unreal.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple');target=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin');retarget=unreal.load_asset(R+'/RTG_PistolSurvivor')
paths=unreal.EditorAssetLibrary.list_assets('/Game/Characters/Mannequins/Anims/Rifle',recursive=True)
assets=[unreal.EditorAssetLibrary.find_asset_data(p) for p in paths if p.split('.')[-1] in ['MF_Rifle_Idle_ADS','MM_Rifle_Fire','MM_Rifle_Reload','MM_Rifle_Equip','MM_Rifle_DryFire','AO_Rifle'] and not unreal.EditorAssetLibrary.does_asset_exist(R+'/Survivor_'+p.split('.')[-1])]
if assets:
 inputs=unreal.IKRetargetBatchOperationInputs()
 for k,v in {'assets_to_retarget':assets,'source_mesh':source,'target_mesh':target,'ik_retarget_asset':retarget,'prefix':'Survivor_','target_path':R,'use_source_path':False,'include_referenced_assets':True,'overwrite_existing_files':False,'retain_additive_flags':True}.items():inputs.set_editor_property(k,v)
 result=unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
 print('RETARGETED',[str(a.package_name) for a in result])
 unreal.EditorAssetLibrary.save_directory(R,only_if_is_dirty=True,recursive=True)
