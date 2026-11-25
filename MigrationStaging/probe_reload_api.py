import unreal
for n in ['EditorLoadingAndSavingUtils','PackageTools','ChooserTable','ChooserSignature']:
 cls=getattr(unreal,n,None)
 if cls:print(n,[m for m in dir(cls) if any(s in m.lower() for s in ['reload','compile','context','edit','load'])])
print(unreal.EditorLoadingAndSavingUtils.reload_packages.__doc__ if hasattr(unreal.EditorLoadingAndSavingUtils,'reload_packages') else '')
