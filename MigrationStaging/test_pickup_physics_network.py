import unreal,time,json
from pathlib import Path
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False);sw=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority());cw=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
cls=unreal.load_asset('/Game/AIExample/Items/BP_ItemPickup').generated_class()
def pistols(w):return sorted([a for a in unreal.GameplayStatics.get_all_actors_of_class(w,cls) if str(a.get_editor_property('ItemDefinition').get_editor_property('ItemID'))=='Weapon.Pistol'],key=lambda a:a.get_actor_location().y)
server=pistols(sw)[0];client=pistols(cw)[0];start=server.get_actor_location();server.set_actor_location(start+unreal.Vector(0,0,300),False,True);server.get_editor_property('PickupMesh').wake_all_rigid_bodies();server.force_net_update()
state={'phase':0,'next':time.monotonic()+.4};report={'checks':{}}
def tick(dt):
 if time.monotonic()<state['next']:return
 if state['phase']==0:
  report['checks']['server_physics_active']=server.get_editor_property('PickupMesh').is_simulating_physics()
  report['checks']['client_follows_lift']=client.get_actor_location().z>start.z+20
  state['phase']=1;state['next']=time.monotonic()+3;return
 report['checks']['server_settled_on_ground']=-2<server.get_actor_location().z<20
 report['checks']['client_matches_settled_server']=(server.get_actor_location()-client.get_actor_location()).length()<5
 report['server']=str(server.get_actor_location());report['client']=str(client.get_actor_location());report['passed']=all(report['checks'].values())
 (Path(unreal.Paths.project_saved_dir())/'EquipmentValidation/ground-physics-multiplayer-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));unreal.unregister_slate_post_tick_callback(physics_net_handle)
physics_net_handle=unreal.register_slate_post_tick_callback(tick)
