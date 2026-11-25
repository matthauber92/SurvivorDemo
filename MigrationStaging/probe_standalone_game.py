import unreal,time,json,traceback
from pathlib import Path
report={};deadline=time.monotonic()+3

def probe_tick(dt):
 if time.monotonic()<deadline:return
 try:
  worlds=[w for w in unreal.ObjectIterator(unreal.World) if unreal.GameplayStatics.get_player_controller(w,0)]
  for w in worlds:
   pc=unreal.GameplayStatics.get_player_controller(w,0);pawn=unreal.GameplayStatics.get_player_pawn(w,0)
   report[w.get_path_name()]={'pc':pc.get_class().get_name(),'pawn':pawn.get_class().get_name(),'components':[c.get_class().get_name() for c in pawn.get_components_by_class(unreal.ActorComponent)]}
   if 'Inventory' in pc.get_class().get_name():
    report[w.get_path_name()]['open_before']=pc.get_editor_property('InventoryOpen')
    pc.call_method('ToggleInventory');report[w.get_path_name()]['open_after']=pc.get_editor_property('InventoryOpen')
    widget=pc.get_editor_property('InventoryWidget')
    report[w.get_path_name()]['widget']=str(widget)
    pc.call_method('CloseInventory')
  report['subsystems']=[]
  for sub in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem):
   report['subsystems'].append({'path':sub.get_path_name(),'has_interaction_context':sub.has_mapping_context(unreal.load_asset('/Game/AIExample/Interaction/IMC_SurvivorInteraction'))})
 except Exception:report['error']=traceback.format_exc()
 (Path(unreal.Paths.project_saved_dir())/'InventoryUIValidation/standalone-probe.json').write_text(json.dumps(report,indent=2))
 unreal.unregister_slate_post_tick_callback(standalone_probe_handle)
standalone_probe_handle=unreal.register_slate_post_tick_callback(probe_tick)

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
