from pathlib import Path
p=Path('MigrationStaging/probe_standalone_game.py');s=p.read_text().replace("'standalone-probe.json'","'standalone-probe2.json'")
s += '''
key_samples=[]
last_sample=None
def sample_keys(dt):
 global last_sample
 try:
  for w in unreal.ObjectIterator(unreal.World):
   p=unreal.GameplayStatics.get_player_controller(w,0)
   if p and 'Inventory' in p.get_class().get_name():
    k=unreal.Key();k.import_text('I')
    sample={'I_down':p.is_input_key_down(k),'open':p.get_editor_property('InventoryOpen'),'cursor':p.get_editor_property('show_mouse_cursor')}
    if sample!=last_sample:
     key_samples.append(sample);last_sample=sample
     (Path(unreal.Paths.project_saved_dir())/'InventoryUIValidation/standalone-key-events.json').write_text(json.dumps(key_samples,indent=2))
 except Exception:pass
standalone_sample_handle=unreal.register_slate_post_tick_callback(sample_keys)
'''
p.write_text(s)
p=Path('MigrationStaging/test_inventory_standalone_probe.ps1');s=p.read_text().replace('standalone-probe.json','standalone-probe2.json');p.write_text(s)
