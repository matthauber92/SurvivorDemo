import unreal,json
from pathlib import Path
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];pc=unreal.GameplayStatics.get_player_controller(w,0);inv=pc.get_editor_property('InventoryComponent')
guns=[a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_asset('/Game/AIExample/Items/BP_ItemPickup').generated_class()) if str(a.get_editor_property('ItemDefinition').get_editor_property('ItemID'))=='Weapon.Pistol']
report={'method':'physical E key in standalone PIE','checks':{'pistol_added_to_backpack':inv.call_method('GetItemQuantity',(unreal.Name('Weapon.Pistol'),))==1,'collected_world_pistol_removed':len(guns)==1,'unique_weapon_instance_created':len(inv.get_editor_property('WeaponInstances'))==1}}
report['passed']=all(report['checks'].values());(Path(unreal.Paths.project_saved_dir())/'EquipmentValidation/ground-pickup-keyboard-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));assert report['passed']
