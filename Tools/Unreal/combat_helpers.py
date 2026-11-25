import unreal,toolset_registry
from editor_toolset.toolsets.blueprint import BlueprintTools as B,ContainerType,_BlueprintCache
R='/Game/Survivor/'
def asset(p):return unreal.load_asset(R+p)
def var(bp,n,t,rep=False,array=False):
 if n not in B.list_variables(bp):
  if isinstance(t,str):B.add_variable(bp,n,t,container_type=ContainerType.ARRAY if array else None)
  else:B.add_object_variable(bp,n,t,container_type=ContainerType.ARRAY if array else None)
 if rep:B.set_variable_replication(bp,n,unreal.BlueprintVariableReplication.REP_NOTIFY)
def fn(bp,n,ins=[],outs=[],locals=[]):
 g=next((g for g in B.list_graphs(bp) if g.get_name()==n),None)
 if not g:
  g=B.add_function_graph(bp,n)
  for inputs,args in [(True,ins),(False,outs)]:
   for k,t in args:
    if isinstance(t,str):B.add_function_param(g,k,t,inputs)
    else:B.add_object_function_param(g,k,t,inputs)
  for k,t in locals:B.add_variable(bp,k,t,graph=g)
 return g
def write(bp,n,code):
 with toolset_registry.tool_raising_exceptions():B.write_graph_dsl(fn(bp,n),code)
 print('COMBAT_GRAPH',bp.get_name(),n)
def save(bp):
 with toolset_registry.tool_raising_exceptions():B.compile_blueprint(bp,warnings_as_errors=True)
 assert bp.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE,(bp.get_name(),str(bp.get_editor_property('status')))
 assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 _BlueprintCache.invalidate(bp)
def pin(n,name,out=False):return next(p.pin_id for p in (B._get_node_info(n).output_pins if out else B._get_node_info(n).input_pins) if p.name==name)
