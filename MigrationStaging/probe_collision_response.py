import unreal
print(unreal.PrimitiveComponent.set_collision_response_to_all_channels.__doc__)
print(unreal.PrimitiveComponent.set_collision_response_to_channel.__doc__)
print([x for x in dir(unreal) if 'CollisionResponse' in x])
print([x for x in dir(unreal.CollisionChannel) if x.isupper()])
