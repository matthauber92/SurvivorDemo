import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter');g=B.get_graph(b,'EventGraph')
for t in ['Animation|Montage|PlaySlotAnimationasDynamicMontage','Animation|Montage|StopSlotAnimation','Niagara|SpawnSystemAttached','Audio|PlaySoundatLocation','Game|Damage|ApplyPointDamage','Transformation|GetSocketLocation','Transformation|GetSocketRotation']:
 q=B.get_node_type_pins(g,t);print('PINS',t,[(p.name,p.type_id,p.value) for p in q.input_pins] if q else None)
print('AO_SAMPLES',[(str(s.get_editor_property('animation')),s.get_editor_property('sample_value')) for s in unreal.load_asset('/Game/AIExample/Combat/Animation/Survivor_AO_Pistol').get_editor_property('sample_data')])
