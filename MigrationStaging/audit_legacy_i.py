import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
for obj in unreal.ObjectIterator(unreal.K2Node_InputKey):
 try:
  key=obj.get_editor_property('input_key')
  if key.export_text()=='I':print('I_CONFLICT',obj.get_path_name(),obj.get_editor_property('consume_input'))
 except Exception as e:print(e)
