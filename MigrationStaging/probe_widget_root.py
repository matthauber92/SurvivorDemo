import unreal
bp=unreal.load_asset('/Game/AIExample/UI/WBP_Inventory');t=unreal.find_object(bp,'WidgetTree');r=unreal.find_object(t,'InventoryRoot')
try:t.set_editor_property('RootWidget',r);print('ROOT_SET',t.get_editor_property('RootWidget'))
except Exception as e:print(e)
print('TOOLS',[n for n in dir(unreal.ToolsetLibrary) if any(x in n for x in ['widget','import','property','text'])])
print('FACTORY',[n for n in dir(unreal) if 'Widget' in n and ('Editor' in n or 'Subsystem' in n)])
