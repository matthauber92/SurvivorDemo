import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();inv=pc.get_editor_property('InventoryComponent')
slot=2;uid=inv.get_editor_property('EquipmentInstances')[slot]
if str(inv.get_editor_property('ActiveWeaponInstance'))!=str(uid):assert inv.call_method('TrySelectWeapon',(slot,uid,inv.get_editor_property('LayoutVersion')))
p.set_actor_location(unreal.Vector(-100,-600,100),False,True);p.character_movement.set_movement_mode(unreal.MovementMode.MOVE_WALKING);pc.set_control_rotation(unreal.Rotator())
assert inv.call_method('TryPistolAction',(1,uid,p.get_actor_location(),unreal.Vector(1,0,0)))
if not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.DebugCameraController):unreal.SystemLibrary.execute_console_command(w,'ToggleDebugCamera',pc)
