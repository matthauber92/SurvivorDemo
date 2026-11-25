import unreal,inspect
from editor_toolset.toolsets.actor import ActorTools as A
print('SPAWN',inspect.signature(A.spawn_actor))
ws=unreal.EditorLevelLibrary.get_pie_worlds(False);print('WORLDS',ws)
if ws:
 w=ws[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();i=pc.get_editor_property('InventoryComponent');m=p.get_component_by_class(unreal.SkeletalMeshComponent)
 if not i.get_editor_property('WeaponInstances'):
  i.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_PistolItem'),1));i.call_method('TryTransferWeapon',(0,10,i.get_editor_property('BackpackInstances')[0],i.get_editor_property('LayoutVersion')))
 if not i.get_editor_property('ActiveWeaponInstance'):i.call_method('TrySelectWeapon',(2,i.get_editor_property('EquipmentInstances')[2],i.get_editor_property('LayoutVersion')))
 hand=m.get_socket_transform('hand_r')
 for n in ['hand_r','weapon_r','index_01_r','middle_01_r','ring_01_r','thumb_01_r','thumb_02_r','pinky_01_r']:print('BONE',n,unreal.MathLibrary.inverse_transform_location(hand,m.get_socket_location(n)))
 print('CAMERA',[(c.get_name(),c.get_class().get_name()) for c in p.get_components_by_class(unreal.SceneComponent)])
