import unreal,toolset_registry
from editor_toolset.toolsets.actor import ActorTools as A
from editor_toolset.toolsets.blueprint import BlueprintTools as B
R='/Game/AIExample/'
bp=unreal.load_asset(R+'Items/BP_ItemPickup');cdo=unreal.get_default_object(bp.generated_class())
mesh=next(c for c in A.get_components(cdo) if isinstance(c,unreal.StaticMeshComponent))
root=A.get_root_component(cdo)
with toolset_registry.tool_raising_exceptions():
 if root!=mesh:assert A.set_parent_component(root,mesh)
 B.compile_blueprint(bp)
cdo=unreal.get_default_object(bp.generated_class());cdo.set_replicate_movement(True)
mesh=next(c for c in A.get_components(cdo) if isinstance(c,unreal.StaticMeshComponent))
mesh.set_collision_profile_name('BlockAllDynamic');mesh.set_enable_gravity(True)
mesh.set_editor_property('body_instance',mesh.get_editor_property('body_instance'))
sm=unreal.load_asset(R+'Weapons/TheHouse/04_Weapons/Pistol/Mesh/SM_Pistol')
sub=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
if sub.get_convex_collision_count(sm)>1:sub.remove_collisions(sm)
if sub.get_simple_collision_count(sm)==0 and sub.get_convex_collision_count(sm)==0:
 assert sub.add_simple_collisions(sm,unreal.ScriptCollisionShapeType.NDOP26)>=0
assert unreal.EditorAssetLibrary.save_loaded_asset(sm,only_if_is_dirty=False)
code='''(fn ApplyDefinitionMesh ()
 (Utilities|IsValid (Variables|Default|GetItemDefinition)
  (:"Is Valid"
   (Components|StaticMesh|SetStaticMesh :self (Variables|Default|GetPickupMesh) :NewMesh (Class|PDAItemDefinition|GetWorldMesh :self (Variables|Default|GetItemDefinition)))
   (if (== (Class|PDAItemDefinition|GetCategory :self (Variables|Default|GetItemDefinition)) "Weapon")
     (Networking|SetReplicateMovement :bInReplicateMovement true)
     (Physics|SetEnableGravity :self (Variables|Default|GetPickupMesh) :bGravityEnabled true)
     (Physics|SetSimulatePhysics :self (Variables|Default|GetPickupMesh) :bSimulate true)))))'''
with toolset_registry.tool_raising_exceptions():B.write_graph_dsl(B.get_graph(bp,'ApplyDefinitionMesh'),code)
B.compile_blueprint(bp,warnings_as_errors=True)
assert bp.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE
unreal.get_default_object(bp.generated_class()).set_replicate_movement(True)
assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
# Put test weapons on the ground in the editor; physics keeps them grounded in play.
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for a in actors.get_all_level_actors():
 if a.get_class()!=bp.generated_class() or not a.get_actor_label().startswith('Equipment_'):continue
 d=a.get_editor_property('ItemDefinition');is_pistol=str(d.get_editor_property('EquipmentType'))=='Sidearm'
 a.set_replicate_movement(True)
 a.set_actor_scale3d(unreal.Vector(1,1,1) if is_pistol else unreal.Vector(.5,.5,.5))
 a.set_actor_rotation(unreal.Rotator(0,0,90) if is_pistol else unreal.Rotator(),False)
 p=a.get_actor_location();a.set_actor_location(unreal.Vector(p.x,p.y,5 if is_pistol else 27),False,True)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
print('PICKUP_COLLISION_AND_PHYSICS_FIXED')
