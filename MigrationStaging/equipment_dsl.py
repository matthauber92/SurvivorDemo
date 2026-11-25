import re
def typed(code):
 code=re.sub(r'\(return \(CallFunction\|RejectEquipment ("[^"]*")\)\)',r'(CallFunction|RejectEquipment \1) (return false)',code)
 strings=['Instance','ExpectedInstance','(Variables|Default|GetSourceInstance)','(Variables|Default|GetTargetInstance)','(Variables|Default|GetSelectedInstance)']
 names=['Kind','ID','(Class|PDAItemDefinition|GetCategory Definition)','(Class|PDAItemDefinition|GetEquipmentType Definition)','(Class|PDAItemDefinition|GetItemID Definition)']
 for op,method in [('==','Equal'),('!=','NotEqual')]:
  for value in strings:code=code.replace('('+op+' '+value+' ','(Utilities|String|'+method+'Exactly(String) '+value+' ')
 code=re.sub(r'\(CallFunction\|([A-Za-z0-9_]+) (?!:)',r'(CallFunction|\1 self ',code)
 return code
