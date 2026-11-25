"""Run after client input has opened the door in two-player listen-server PIE."""
import unreal,json,time
from pathlib import Path
root='/Game/AIExample/Interaction/'
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
dc=unreal.load_class(None,root+'BP_InteractionTestDoor.BP_InteractionTestDoor_C')
cc=unreal.load_class(None,root+'BP_InteractionComponent.BP_InteractionComponent_C')
server=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
client=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
cp=unreal.GameplayStatics.get_player_pawn(client,0)
pc=unreal.GameplayStatics.get_player_controller(client,0)
comp=cp.get_component_by_class(cc)
sp=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(server,unreal.Pawn) if not p.is_locally_controlled())
sc=sp.get_component_by_class(cc)
host=unreal.GameplayStatics.get_player_pawn(server,0)
doors=[unreal.GameplayStatics.get_all_actors_of_class(w,dc)[0] for w in [server,client]]
action=unreal.load_asset(root+'IA_SurvivorInteract')
subsystems=[s for s in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if 'Transient' in s.get_path_name()]
report={'mode':'two-player listen server','checks':{}}
def check(name,value):
    report['checks'][name]=bool(value)
    unreal.log('INTERACTION_CHECK '+name+' '+str(bool(value)))
def state(opened):
    return all(d.get_editor_property('IsOpen')==opened and abs(d.get_editor_property('DoorHinge').get_editor_property('relative_rotation').yaw-(90 if opened else 0))<0.1 for d in doors)
def inject():
    for s in subsystems:s.inject_input_vector_for_action(action,unreal.Vector(1,0,0),[],[])
check('client_input_opens_and_replicates_visual',state(True))
check('input_context_active',all(s.has_mapping_context(unreal.load_asset(root+'IMC_SurvivorInteraction')) for s in subsystems))
check('hud_class',pc.get_hud().get_class().get_name()=='BP_InteractionHUD_C')
pc.set_control_rotation(unreal.Rotator(pitch=0,yaw=-26.565,roll=0))
validation={'phase':0,'next':time.monotonic()+1}
def tick(dt):
    if time.monotonic()<validation['next']:return
    try:
        phase=validation['phase']
        if phase==0:
            check('client_close_prompt',str(comp.get_editor_property('PromptText'))=='Press E to Close Door')
            inject()
        elif phase==1:
            check('client_input_closes_and_replicates_visual',state(False))
            sp.set_actor_location(unreal.Vector(-650,300,90),False,True)
            host.set_actor_location(unreal.Vector(-180,0,90),False,True)
            unreal.GameplayStatics.get_player_controller(server,0).set_control_rotation(unreal.Rotator(0,0,0))
        elif phase==2:
            hc=host.get_component_by_class(cc)
            check('host_open_prompt',str(hc.get_editor_property('PromptText'))=='Press E to Open Door')
            check('distant_client_prompt_hidden',str(comp.get_editor_property('PromptText'))=='')
            check('server_rejects_out_of_range',not sc.call_method('ValidateTarget',(doors[0],unreal.Vector(-480,0,100),unreal.Vector(1,0,0))))
            inject()
        elif phase==3:
            check('host_input_opens_and_replicates_visual',state(True))
            # Direct authoritative calls verify the per-door cooldown independently of input timing.
            accepted=doors[0].call_method('TryInteract',(host,))
            rejected=not doors[0].call_method('TryInteract',(host,))
            check('cooldown_rejects_immediate_repeat',accepted and rejected)
            hc=host.get_component_by_class(cc)
            # Floor blocks this downward trace, so it must not validate the door.
            check('server_rejects_wrong_line_of_sight',not hc.call_method('ValidateTarget',(doors[0],unreal.Vector(-180,0,100),unreal.Vector(0,0,-1))))
            check('server_rejects_spoofed_view_origin',not hc.call_method('ValidateTarget',(doors[0],unreal.Vector(-2000,0,100),unreal.Vector(1,0,0))))
            report['passed']=all(report['checks'].values())
            (Path(unreal.Paths.project_saved_dir())/'InteractionValidation/play-result.json').write_text(json.dumps(report,indent=2))
            unreal.log('INTERACTION_RESULT '+json.dumps(report))
            unreal.unregister_slate_post_tick_callback(interaction_validation_handle)
        validation['phase']+=1
        validation['next']=time.monotonic()+1
    except Exception as e:
        report['error']=str(e);report['passed']=False
        (Path(unreal.Paths.project_saved_dir())/'InteractionValidation/play-result.json').write_text(json.dumps(report,indent=2))
        unreal.unregister_slate_post_tick_callback(interaction_validation_handle)
        unreal.log_error(str(e))
interaction_validation_handle=unreal.register_slate_post_tick_callback(tick)
