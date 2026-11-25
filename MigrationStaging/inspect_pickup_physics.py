import unreal
from editor_toolset.toolsets.actor import ActorTools as A
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Items/BP_ItemPickup');cdo=unreal.get_default_object(b.generated_class())
print('ROOT',A.get_root_component(cdo))
for c in A.get_components(cdo):
 print('COMP',c.get_name(),c.get_class().get_name())
 if isinstance(c,unreal.StaticMeshComponent):print('MESH',c.get_editor_property('mobility'),c.get_collision_profile_name(),c.is_simulating_physics(),c.get_editor_property('relative_scale3d'))
sm=unreal.load_asset('/Game/AIExample/Weapons/TheHouse/04_Weapons/Pistol/Mesh/SM_Pistol')
sub=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
print('COLLISION',sub.get_simple_collision_count(sm),sm.get_editor_property('body_setup').get_editor_property('collision_trace_flag'))
print('BOUNDS',sm.get_bounds())
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 if a.get_class()==b.generated_class():print('PICKUP',a.get_actor_label(),a.get_actor_location(),a.get_actor_scale3d(),a.get_editor_property('PickupMesh').get_world_scale())
g=B.get_graph(b,'ApplyDefinitionMesh')
for term in ['SetSimulatePhysics','SetEnableGravity','SetReplicateMovement']:print(term,list(B.find_node_types(g,term,[])))
