import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/UI/WBP_Inventory')
for n,k in [('ToggleKey','I'),('CloseKey','Escape')]:
 if n not in B.list_variables(b):B.add_struct_variable(b,n,unreal.load_object(None,'/Script/InputCore.Key'))
 B.compile_blueprint(b);key=unreal.Key();key.import_text(k);unreal.get_default_object(b.generated_class()).set_editor_property(n,key)
