import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
R='/Game/AIExample/'
for n in ['Items/PDA_ItemDefinition','Items/BP_InventoryComponent','Items/BP_ItemPickup','Items/BP_InventoryPlayerController','UI/WBP_Inventory','UI/BP_InventoryDragOperation','UI/WBP_InventoryDragVisual','UI/WBP_InventoryDragProxy']:
 b=unreal.load_asset(R+n);B.compile_blueprint(b,warnings_as_errors=True);assert b.get_editor_property('status')==unreal.BlueprintStatus.BS_UP_TO_DATE,n
 assert unreal.EditorAssetLibrary.save_loaded_asset(b,only_if_is_dirty=False)
level=R+'Maps/Lvl_EquipmentTest'
created=False
ls=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not unreal.EditorAssetLibrary.does_asset_exist(level):
 assert ls.load_level(R+'Maps/Lvl_PickupTest')
 assert unreal.EditorLoadingAndSavingUtils.save_map(unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world(),level);created=True
assert ls.load_level(level)
if True:
 actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
 labels={a.get_actor_label() for a in actors.get_all_level_actors()}
 for i,name in enumerate(['DA_PistolItem','DA_PistolItem','DA_EquipmentTestLongGun','DA_EquipmentTestLongGun']):
  if 'Equipment_'+str(i) in labels:continue
  a=actors.spawn_actor_from_class(unreal.load_asset(R+'Items/BP_ItemPickup').generated_class(),unreal.Vector(-100,-600+i*140,100))
  a.set_actor_label('Equipment_'+str(i));a.set_editor_property('ItemDefinition',unreal.load_asset(R+'Items/'+name));a.set_editor_property('Quantity',1);a.call_method('UserConstructionScript')
 assert ls.save_current_level()
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.LevelEditorPlaySettings'))
unreal.ToolsetLibrary.set_object_properties(s,json.dumps({'playNetMode':'PIE_Standalone','playNumberOfClients':1,'runUnderOneProcess':True,'newWindowWidth':1280,'newWindowHeight':800}))
print('EQUIPMENT_TEST_MAP_READY')
