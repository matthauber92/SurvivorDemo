import unreal,toolset_registry
from editor_toolset.toolsets.blueprint import BlueprintTools as B,_BlueprintCache
for path in ['/Game/Blueprints/SandboxCharacter_CMC_ABP','/Game/AIExample/Combat/Animation/ABP_SurvivorCombat']:
 bp=unreal.load_asset(path);_BlueprintCache.invalidate(bp)
 with toolset_registry.tool_raising_exceptions():
  for g in B.list_graphs(bp):
   for old in list(B.find_nodes(g)):
    info=B._get_node_info(old)
    if 'EvaluateChooser:' not in info.type_id:continue
    print('RECREATE',path,g.get_name(),info.type_id)
    new=B.create_node(g,'Animation|EvaluateChooser',info.position)
    for prop in ['mode','struct_output_mode','return_soft_object_reference']:
     try:new.set_editor_property(prop,old.get_editor_property(prop))
     except Exception:pass
    new.set_editor_property('chooser',old.get_editor_property('chooser'))
    ni=B._get_node_info(new)
    for outs,opins,npins in [(False,info.input_pins,ni.input_pins),(True,info.output_pins,ni.output_pins)]:
     for op in opins:
      if not op.connected_pins:continue
      np=next((p for p in npins if p.name==op.name),None)
      if not np:continue
      for other in list(op.connected_pins):
       if outs:B.break_pins(op.pin_id,other);B.connect_pins(np.pin_id,other)
       else:B.break_pins(other,op.pin_id);B.connect_pins(other,np.pin_id)
    B.delete_node(old)
  B.compile_blueprint(bp,warnings_as_errors=True)
  assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 print('STATUS',bp.get_editor_property('status'))
