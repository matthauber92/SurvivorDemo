import unreal,json
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();c=p.get_editor_property('InteractionComponent');inv=pc.get_editor_property('InventoryComponent')
checks={}
def check(n,v):
 checks[n]=bool(v)
 print(n,bool(v))
 assert v,n
check('idle_camera_250',abs(p.get_editor_property('ShoulderBoom').get_editor_property('target_arm_length')-250)<1)
a=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Items/BP_ItemPickup.BP_ItemPickup_C')) if a.get_editor_property('ItemDefinition').get_name()=='DA_HandgunAmmo')
loc=a.get_actor_location();p.set_actor_location(loc+unreal.Vector(-160,0,0),False,True)
for distance in [250,350,600]:
 origin=p.get_actor_location()+unreal.Vector(-distance,65,45);direction=unreal.MathLibrary.normal(loc-origin)
 check('nearby_pickup_camera_'+str(distance),c.call_method('ValidateTarget',(a,origin,direction)))
origin=p.get_actor_location()+unreal.Vector(-1000,65,45)
check('reject_remote_camera',not c.call_method('ValidateTarget',(a,origin,unreal.MathLibrary.normal(loc-origin))))
p.set_actor_location(loc+unreal.Vector(-350,0,0),False,True)
origin=p.get_actor_location()+unreal.Vector(-250,65,45)
check('reject_out_of_reach',not c.call_method('ValidateTarget',(a,origin,unreal.MathLibrary.normal(loc-origin))))
check('out_of_reach_not_collected',not a.call_method('TryInteract',(p,)))
p.set_actor_location(loc+unreal.Vector(-160,0,0),False,True)
definition=a.get_editor_property('ItemDefinition');item=definition.get_editor_property('ItemId');amount=a.get_editor_property('Quantity');before=inv.call_method('GetItemQuantity',(item,))
check('collect_succeeds',a.call_method('TryInteract',(p,)))
check('inventory_receives_exact_amount',inv.call_method('GetItemQuantity',(item,))==before+amount)
# Set up an unobstructed, nearby target to test the actual focus/request path next tick.
target=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Items/BP_ItemPickup.BP_ItemPickup_C')) if a.get_editor_property('ItemDefinition').get_name()=='DA_FirstAidKit')
target.set_actor_location(unreal.Vector(1000,1000,130),False,True)
p.set_actor_location(unreal.Vector(840,1000,90),False,True)
pc.set_control_rotation(unreal.Rotator(0,0,0))
Path(unreal.Paths.project_saved_dir(),'camera-pickup-checks.json').write_text(json.dumps(checks,indent=2))
