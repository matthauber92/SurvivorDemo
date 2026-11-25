import unreal,ast,toolset_registry
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A
bp=unreal.load_asset('/Game/AIExample/Items/BP_ItemPickup')
source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/fix_pickup_physics.py').read_text())
code=next(ast.literal_eval(n.value) for n in source.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='code' for t in n.targets))
code=code.replace('(Networking|SetReplicateMovement', '''(Collision|SetCollisionResponsetoChannel :self (Variables|Default|GetPickupMesh) :Channel "ECC_Pawn" :NewResponse "ECR_Ignore")
     (Collision|SetCollisionResponsetoChannel :self (Variables|Default|GetPickupMesh) :Channel "ECC_Camera" :NewResponse "ECR_Ignore")
     (Networking|SetReplicateMovement''')
with toolset_registry.tool_raising_exceptions():B.write_graph_dsl(B.get_graph(bp,'ApplyDefinitionMesh'),code)
B.compile_blueprint(bp,warnings_as_errors=True)
assert bp.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE
mesh=next(c for c in A.get_components(unreal.get_default_object(bp.generated_class())) if isinstance(c,unreal.StaticMeshComponent))
mesh.set_editor_property('can_character_step_up_on',unreal.CanBeCharacterBase.ECB_NO)
assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
# Camera traces block scenery; loose weapons ignore both Pawn and Camera.
# Use the existing Camera trace channel so foot IK ignores those weapons too.
anim=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP')
node=unreal.find_object(anim,'AnimGraph.AnimGraphNode_FootPlacement_0')
settings=node.get_editor_property('node');traces=settings.get_editor_property('trace_settings')
traces.set_editor_property('simple_trace_channel',unreal.TraceTypeQuery.ECC_CAMERA)
traces.set_editor_property('complex_trace_channel',unreal.TraceTypeQuery.ECC_CAMERA)
settings.set_editor_property('trace_settings',traces);node.set_editor_property('node',settings)
with toolset_registry.tool_raising_exceptions():B.compile_blueprint(anim,warnings_as_errors=True)
assert anim.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE
assert unreal.EditorAssetLibrary.save_loaded_asset(anim,only_if_is_dirty=False)
print('LOOSE_WEAPONS_IGNORE_CHARACTER_AND_FOOT_TRACES')
