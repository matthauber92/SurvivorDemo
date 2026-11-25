import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Items/BP_ItemPickup')
B.set_variable_replication(bp,'ItemDefinition',unreal.BlueprintVariableReplication.NONE)
if 'DefinitionPath' not in B.list_variables(bp):B.add_struct_variable(bp,'DefinitionPath',unreal.load_object(None,'/Script/CoreUObject.SoftObjectPath'))
B.set_variable_replication(bp,'DefinitionPath',unreal.BlueprintVariableReplication.REP_NOTIFY)
meshgraph=next((g for g in B.list_graphs(bp) if g.get_name()=='ApplyDefinitionMesh'),None) or B.add_function_graph(bp,'ApplyDefinitionMesh')
B.write_graph_dsl(meshgraph,'''(fn ApplyDefinitionMesh ()
 (Utilities|IsValid (Variables|Default|GetItemDefinition)
  (:"Is Valid" (Components|StaticMesh|SetStaticMesh :self (Variables|Default|GetPickupMesh) :NewMesh (Class|PDAItemDefinition|GetWorldMesh :self (Variables|Default|GetItemDefinition))))
  (:"Is Not Valid")))''')
B.write_graph_dsl(B.get_graph(bp,'OnRep_DefinitionPath'),'''(fn OnRep_DefinitionPath ()
 (bind Definition (Utilities|Casting|CastToPDA_ItemDefinition :Object
  (Utilities|LoadAssetBlocking :Asset (Utilities|ToSoftObjectReference (Variables|Default|GetDefinitionPath))))
  (:then
   (Variables|Default|SetItemDefinition Definition)
   (CallFunction|ApplyDefinitionMesh))
  (:CastFailed)))''')
B.write_graph_dsl(B.get_graph(bp,'EventGraph'),'''(event AddEvent|EventBeginPlay
 (if (Networking|HasAuthority)
  (Variables|Default|SetDefinitionPath (Utilities|GetSoftObjectPath (Variables|Default|GetItemDefinition))))
 (CallFunction|ApplyDefinitionMesh))''')
B.compile_blueprint(bp)
print('ONREP',B.read_graph_dsl(B.get_graph(bp,'OnRep_DefinitionPath')))
unreal.EditorAssetLibrary.save_loaded_asset(bp)
print('DEFINITION_PATH_REPLICATION_SAVED')

