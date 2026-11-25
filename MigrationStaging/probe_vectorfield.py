import unreal
field=unreal.load_asset('/Niagara/VectorFields/Assets/TilingCurl32')
print(field.get_class().__doc__)
for n in ['allow_cpu_access','size_x','size_y','size_z']:
 try:print(n,field.get_editor_property(n))
 except Exception as e:print(n,str(e))
print('NIAGARA EDIT',[(n,[m for m in dir(getattr(unreal,n)) if 'compile' in m.lower()]) for n in dir(unreal) if 'Niagara' in n and any(s in n for s in ['Library','Editor'])])
