import unreal,json
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();c=p.get_editor_property('InteractionComponent');inv=pc.get_editor_property('InventoryComponent');cam=unreal.GameplayStatics.get_player_camera_manager(w,0)
target=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Items/BP_ItemPickup.BP_ItemPickup_C')) if a.get_editor_property('ItemDefinition').get_name()=='DA_FirstAidKit')
origin=cam.get_camera_location();direction=unreal.MathLibrary.get_forward_vector(cam.get_camera_rotation());target.set_actor_location(origin+direction*410,False,True)
data=Path(unreal.Paths.project_saved_dir(),'camera-pickup-checks.json');checks=json.loads(data.read_text())
def check(n,v):
 checks[n]=bool(v);print(n,bool(v));data.write_text(json.dumps(checks,indent=2));assert v,n
c.call_method('UpdateFocus')
check('camera_focus_finds_pickup',c.get_editor_property('FocusedActor')==target)
check('pickup_prompt_present','Press E' in str(c.get_editor_property('PromptText')))
item=target.get_editor_property('ItemDefinition').get_editor_property('ItemId');before=inv.call_method('GetItemQuantity',(item,));quantity=target.get_editor_property('Quantity')
c.call_method('RequestInteraction')
check('request_interaction_adds_item',inv.call_method('GetItemQuantity',(item,))==before+quantity)
c.call_method('UpdateFocus');check('collected_pickup_clears_focus',c.get_editor_property('FocusedActor')!=target)
c.call_method('RequestInteraction');check('repeat_request_no_duplicate',inv.call_method('GetItemQuantity',(item,))==before+quantity)
