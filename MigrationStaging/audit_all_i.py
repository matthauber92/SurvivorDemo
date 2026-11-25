import unreal
print([n for n in dir(unreal) if 'K2Node' in n and ('Input' in n or 'Key' in n)])
for obj in unreal.ObjectIterator(unreal.EdGraphNode):
 if any(t in obj.get_class().get_name() for t in ['InputKey','DebugKey']):
  try:
   key=obj.get_editor_property('input_key')
   if key.export_text()=='I':print('I',obj.get_path_name())
  except:pass
