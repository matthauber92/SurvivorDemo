import unreal
c=unreal.load_asset('/Game/AIExample/Interaction/IMC_SurvivorInteraction')
print('BEFORE',[(m.get_editor_property('action').get_path_name(),m.get_editor_property('key').export_text()) for m in c.get_editor_property('default_key_mappings').get_editor_property('mappings')])
for path,keyname in [('/Game/AIExample/UI/IA_ToggleInventory','I'),('/Game/AIExample/Interaction/IA_SurvivorInteract','E')]:
 action=unreal.load_asset(path);c.unmap_all_keys_from_action(action)
 key=unreal.Key();key.import_text(keyname);c.map_key(action,key)
assert unreal.EditorAssetLibrary.save_loaded_asset(c,only_if_is_dirty=False)
print('AFTER',[(m.get_editor_property('action').get_path_name(),m.get_editor_property('key').export_text()) for m in c.get_editor_property('default_key_mappings').get_editor_property('mappings')])
