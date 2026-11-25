import unreal
from editor_toolset.toolsets.actor import ActorTools as A
b=unreal.load_asset('/Game/AIExample/Items/BP_ItemPickup')
for c in A.get_components(unreal.get_default_object(b.generated_class())):
 if isinstance(c,unreal.SphereComponent):print('TEMPLATE',c.get_unscaled_sphere_radius(),c.get_collision_enabled(),c.get_editor_property('absolute_scale'))
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,b.generated_class()):
 c=a.get_editor_property('WeaponInteractionTarget');print('RUNTIME',a.get_name(),c.get_unscaled_sphere_radius(),c.get_scaled_sphere_radius(),c.get_collision_enabled(),c.get_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY))
