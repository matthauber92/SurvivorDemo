import unreal,json
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0]
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();c=p.get_editor_property('InteractionComponent')
pickups=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Items/BP_ItemPickup.BP_ItemPickup_C'))
print('WORLD',w.get_path_name(),'PAWN',p.get_path_name(),'COMP',c.get_path_name())
print('PICKUPS',[(a.get_name(),str(a.get_actor_location()),str(a.get_editor_property('ItemDefinition'))) for a in pickups])
print('FOCUS',c.get_editor_property('FocusedActor'),c.get_editor_property('PromptText'))
for a in pickups[:5]:
 loc=a.get_actor_location();p.set_actor_location(loc+unreal.Vector(-160,0,90),False,True)
 origin=loc+unreal.Vector(-450,65,170);direction=unreal.MathLibrary.normal(loc-origin)
 print('VALIDATE',a.get_name(),c.call_method('ValidateTarget',(a,origin,direction)), 'PROMPT',a.call_method('GetInteractionPrompt',(p,)))
 print('TRY',a.call_method('TryInteract',(p,)))
