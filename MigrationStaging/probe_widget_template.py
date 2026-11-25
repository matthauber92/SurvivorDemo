import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/Input/Touch/UI_TouchSimple');t=unreal.find_object(b,'WidgetTree')
print('GRAPHS',[(g.get_name()) for g in B.list_graphs(b)])
for w in unreal.ObjectIterator(unreal.Widget):
 if w.get_outer()==t: print('W',w.get_name(),w.get_class().get_name(),w.get_parent())
w=unreal.new_object(unreal.TextBlock,outer=unreal.find_object(unreal.load_asset('/Game/AIExample/UI/WBP_Inventory'),'WidgetTree'),name='ProbeText')
for prop in ['bIsVariable','is_variable']:
 try:w.set_editor_property(prop,True);print('VAR_OK',prop)
 except Exception as e:print(e)
