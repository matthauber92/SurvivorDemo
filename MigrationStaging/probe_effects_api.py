import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Combat/Animation/ABP_SurvivorCombat');g=B.get_graph(b,'AnimGraph')
info=B.get_node_type_pins(g,"Animation|BlendSpaces|AimOffsetPlayer'Survivor_AO_Pistol'");print('AO_PINS',[(p.name,p.type_id,p.value) for p in info.input_pins])
for cl in [unreal.AnimationLibrary.add_animation_notify_event,unreal.StaticMeshSocket,unreal.AnimNotify_PlaySound]:print('API',cl.__doc__)
print('ATTEN', [x for x in dir(unreal) if 'Attenuation' in x and 'Factory' in x])
