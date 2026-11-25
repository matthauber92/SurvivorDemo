import unreal
mesh=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin')
print('MESH',mesh.get_path_name(),'SKELETON',mesh.get_editor_property('skeleton').get_path_name())
for cls in ['PreviewAssetAttachContainer','PreviewAttachedObjectPair']:
 c=getattr(unreal,cls,None);print('PREVIEW_TYPE',cls,c,c.__doc__ if c else '')
try:print('PREVIEW_VALUE',mesh.get_editor_property('preview_attached_asset_container'))
except Exception as e:print('PREVIEW_ERROR',str(e))
