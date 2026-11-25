import unreal,json
from pathlib import Path
assert not (Path(unreal.Paths.project_saved_dir())/'shotgun-socket-fit.json').exists(), 'One-time fitting already applied; edit ShotgunGrip_R visually to preserve later socket edits.'
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Character) if 'Survivor' in p.get_class().get_name());m=p.mesh
asset=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SKM_UEFN_Mannequin');socket=asset.find_socket('ShotgunGrip_R')
before=socket.get_editor_property('relative_location');hand=m.get_socket_transform('hand_r',unreal.RelativeTransformSpace.RTS_WORLD)
delta=unreal.MathLibrary.inverse_transform_direction(hand,unreal.Vector(4,0,4))
socket.set_editor_property('relative_location',before+delta)
(Path(unreal.Paths.project_saved_dir())/'shotgun-socket-fit.json').write_text(json.dumps({'before':str(before),'after':str(before+delta),'world_adjustment_cm':[4,0,4]},indent=2))
print('SHOTGUN_SOCKET_FITTED',before+delta)
