import unreal,json
from pathlib import Path
root='/Game/AIExample/Interaction/'
context=unreal.load_asset(root+'IMC_SurvivorInteraction')
action=unreal.load_asset(root+'IA_SurvivorInteract')
key=unreal.Key()
assert key.import_text('E') and unreal.InputLibrary.key_is_valid(key)
context.unmap_all()
context.map_key(action,key)
assert unreal.EditorAssetLibrary.save_loaded_asset(context)
mappings=context.get_editor_property('default_key_mappings').get_editor_property('mappings')
assert len(mappings)==1
assert unreal.InputLibrary.equal_equal_key_key(mappings[0].get_editor_property('key'),key)
print('SAVED_MAPPING',mappings[0].export_text())
