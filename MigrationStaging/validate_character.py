import unreal
import json
from pathlib import Path

worlds = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
pawn = unreal.GameplayStatics.get_player_pawn(worlds, 0)
controller = unreal.GameplayStatics.get_player_controller(worlds, 0)
print('PAWN', pawn.get_path_name(), 'CONTROLLER', controller.get_path_name())
print('POSITION', pawn.get_actor_location(), 'MESH', pawn.mesh.skeletal_mesh_asset, 'ANIM', pawn.mesh.get_anim_instance())
print('CAMERA', controller.get_view_target(), controller.player_camera_manager.get_camera_location())
print('MOVEMENT', pawn.character_movement.movement_mode)
assert pawn.get_class().get_name() == 'BP_SurvivorCharacter_C'
assert pawn.get_controller() == controller
assert pawn.mesh.get_anim_instance() is not None
assert controller.get_view_target() == pawn
pawn.set_actor_location(unreal.Vector(0, -500, 90), False, True)
validation = {'phase': 'move', 'elapsed': 0.0, 'start': pawn.get_actor_location(), 'max_z': pawn.get_actor_location().z}

def validate_tick(delta):
    try:
        validation['elapsed'] += delta
        loc = pawn.get_actor_location()
        validation['max_z'] = max(validation['max_z'], loc.z)
        if validation['phase'] == 'move':
            pawn.add_movement_input(unreal.Vector(1, 0, 0), 1.0)
            if validation['elapsed'] > 2.0:
                validation['distance'] = (loc - validation['start']).length()
                validation['jump_start_z'] = loc.z
                pawn.jump()
                validation['phase'] = 'jump'
                validation['elapsed'] = 0.0
        elif validation['elapsed'] > 3.0:
            pawn.stop_jumping()
            result = {
                'pawn': pawn.get_class().get_name(),
                'animation_class': pawn.mesh.get_anim_instance().get_class().get_name(),
                'movement_distance_cm': validation['distance'],
                'jump_height_cm': validation['max_z'] - validation['jump_start_z'],
                'landed': str(pawn.character_movement.movement_mode),
                'camera_tracks_pawn': controller.get_view_target() == pawn,
                'camera_distance_cm': (controller.player_camera_manager.get_camera_location() - loc).length(),
            }
            result['passed'] = result['movement_distance_cm'] > 100 and result['jump_height_cm'] > 20 and pawn.character_movement.movement_mode == unreal.MovementMode.MOVE_WALKING and result['camera_tracks_pawn']
            (Path(unreal.Paths.project_saved_dir()) / 'GASPValidation/play-result.json').write_text(json.dumps(result, indent=2))
            unreal.log('SURVIVOR_PLAY_RESULT ' + json.dumps(result))
            unreal.unregister_slate_post_tick_callback(validation_handle)
    except Exception as exc:
        unreal.log_error(str(exc))
        unreal.unregister_slate_post_tick_callback(validation_handle)

validation_handle = unreal.register_slate_post_tick_callback(validate_tick)
