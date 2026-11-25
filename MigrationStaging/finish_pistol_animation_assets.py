import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
bp=asset('Combat/Animation/ABP_SurvivorCombat');g=B.get_graph(bp,'AnimGraph')
with toolset_registry.tool_raising_exceptions():
 aoasset=asset('Combat/Animation/Survivor_AO_Pistol')
 print('AO_AXES',[(p.get_editor_property('display_name'),p.get_editor_property('min'),p.get_editor_property('max')) for p in aoasset.get_editor_property('blend_parameters')])
 if not any(isinstance(n,unreal.AnimGraphNode_RotationOffsetBlendSpace) for n in B.find_nodes(g)):
  slot=next(n for n in B.find_nodes(g) if isinstance(n,unreal.AnimGraphNode_Slot) and str(n.get_editor_property('node').get_editor_property('slot_name'))=='PistolUpperBody')
  incoming=next(p for p in B._get_node_info(slot).input_pins if p.name=='Source').connected_pins[0]
  ao=B.create_node(g,"Animation|BlendSpaces|AimOffsetPlayer'Survivor_AO_Pistol'",unreal.IntPoint(2050,400))
  pitch=B.create_node(g,'Variables|Default|GetPistolAimPitch',unreal.IntPoint(1850,650))
  B.break_pins(incoming,pin(slot,'Source'));B.connect_pins(incoming,pin(ao,'BasePose'));B.connect_pins(pin(ao,'Pose',True),pin(slot,'Source'))
  # The template aim-offset uses vertical pitch on its Y axis.
  axes=aoasset.get_editor_property('blend_parameters');axis='Y' if 'pitch' in str(axes[1].get_editor_property('display_name')).lower() else 'X'
  B.connect_pins(B._get_node_info(pitch).output_pins[0].pin_id,pin(ao,axis))
 save(bp)
 # Spatial sound profiles keep remote reloads and shots attached to their source.
 at=unreal.AssetToolsHelpers.get_asset_tools()
 atten=asset('Combat/SA_Pistol') or at.create_asset('SA_Pistol',R+'Combat',unreal.SoundAttenuation,unreal.SoundAttenuationFactory())
 settings=atten.get_editor_property('attenuation');settings.set_editor_property('attenuate',True);settings.set_editor_property('spatialize',True);settings.set_editor_property('attenuation_shape_extents',unreal.Vector(150,0,0));settings.set_editor_property('falloff_distance',3500);atten.set_editor_property('attenuation',settings);unreal.EditorAssetLibrary.save_loaded_asset(atten,only_if_is_dirty=False)
 snd=R+'Weapons/TheHouse/06_SFX/GunSFX/Pistol/'
 reload=asset('Combat/Animation/Survivor_MM_Pistol_Reload')
 track='PistolReloadAudio'
 if unreal.AnimationLibrary.is_valid_anim_notify_track_name(reload,track):unreal.AnimationLibrary.remove_animation_notify_events_by_track(reload,track)
 else:unreal.AnimationLibrary.add_animation_notify_track(reload,track)
 for t,name in [(0.40,'Pistol_Remove_Magazine_Cue'),(1.10,'Pistol_Add_Magazine_Cue'),(1.65,'Pistol_Cocking_Slide_Cue')]:
  sound=unreal.load_asset(snd+'Reload/'+name)
  sound.set_editor_property('attenuation_settings',atten);unreal.EditorAssetLibrary.save_loaded_asset(sound,only_if_is_dirty=False)
  notify=unreal.AnimationLibrary.add_animation_notify_event(reload,track,t,unreal.AnimNotify_PlaySound)
  notify.set_editor_property('sound',sound);notify.set_editor_property('attach_name','PistolGrip_R');notify.set_editor_property('follow',True)
 unreal.EditorAssetLibrary.save_loaded_asset(reload,only_if_is_dirty=False)
 # Dedicated muzzle socket; the muzzle flash never uses a hard-coded world offset.
 mesh=asset('Weapons/TheHouse/04_Weapons/Pistol/Mesh/SM_Pistol')
 if not mesh.find_socket('Muzzle'):
  socket=unreal.new_object(unreal.StaticMeshSocket,outer=mesh);socket.set_editor_property('socket_name','Muzzle');socket.set_editor_property('relative_location',unreal.Vector(11.8,0,6.7));mesh.add_socket(socket)
 unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
 print('PISTOL_AIM_RELOAD_AUDIO_MUZZLE_READY')
