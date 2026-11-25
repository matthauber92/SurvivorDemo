import unreal
ctx=unreal.load_asset('/Game/AIExample/Interaction/IMC_SurvivorInteraction')
print('MAPPING_METHODS',[n for n in dir(ctx) if 'mapping' in n])
for m in ctx.get_editor_property('mappings'):
    print('MAPPING',m.export_text())
key=unreal.Key();result=key.import_text('(KeyName="E")')
print('IMPORT_RESULT',result,'KEY',key.export_text())
print('KEY_API',[n for n in dir(unreal.InputLibrary) if 'key' in n])
print('DEFAULT',ctx.get_editor_property('default_key_mappings'))
for txt in ['E','(KeyName="E")']:
    k=unreal.Key();k.import_text(txt)
    print('TEST',txt,k.export_text(),unreal.InputLibrary.key_is_valid(k),unreal.InputLibrary.key_get_display_name(k))
