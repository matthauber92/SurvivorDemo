import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
root='/Game/AIExample/Interaction'
comp=unreal.load_asset(root+'/BP_InteractionComponent')
if 'InputReady' not in B.list_variables(comp): B.add_variable(comp,'InputReady','bool')
g=B.add_function_graph(comp,'InitializeLocalInput')
B.write_graph_dsl(g,'''(fn InitializeLocalInput ()
 (if (not (Variables|Default|GetInputReady))
  (if (Pawn|IsLocallyControlled :self (Variables|Default|GetOwnerPawn))
   (bind PC (Utilities|Casting|CastToPlayerController :Object (Pawn|GetController :self (Variables|Default|GetOwnerPawn)))
    (:then
     (Input|AddMappingContext
      :self (PlayerController|LocalPlayerSubsystems|GetEnhancedInputLocalPlayerSubsystem :PlayerController PC)
      :MappingContext "/Game/AIExample/Interaction/IMC_SurvivorInteraction.IMC_SurvivorInteraction" :Priority 1)
     (Variables|Default|SetInputReady true))
    (:CastFailed)))))''')
# Insert initialization before focus without replacing the existing RPC event.
eg=B.get_graph(comp,'EventGraph')
tick=next(n for n in B.find_nodes(eg) if B._get_node_info(n).type_id=='AddEvent|EventTick') if False else None
for n in B.find_nodes(eg):
    i=B._get_node_info(n)
    if i.type_id.endswith('|EventTick'):
        tick=n;break
assert tick
init=B.create_node(eg,'CallFunction|InitializeLocalInput',unreal.IntPoint(300,700))
ti=B._get_node_info(tick);ii=B._get_node_info(init)
tp=next(p for p in ti.output_pins if p.type_id=='Exec')
ip=next(p for p in ii.input_pins if p.type_id=='Exec')
op=next(p for p in ii.output_pins if p.type_id=='Exec')
for target in list(tp.connected_pins):
    B.break_pins(tp.pin_id,target);B.connect_pins(op.pin_id,target)
B.connect_pins(tp.pin_id,ip.pin_id)
B.compile_blueprint(comp);unreal.EditorAssetLibrary.save_loaded_asset(comp)
child=unreal.load_asset(root+'/BP_SurvivorInteractionCharacter')
cg=B.get_graph(child,'EventGraph')
event=B.create_node(cg,'Input|EnhancedActionEvents|IA_SurvivorInteract',unreal.IntPoint(0,900))
call=B.create_node(cg,'Class|BPInteractionComponent|RequestInteraction',unreal.IntPoint(400,900))
getter=B.create_node(cg,'Variables|Default|GetInteractionComponent',unreal.IntPoint(160,1100))
ei=B._get_node_info(event);ci=B._get_node_info(call);gi=B._get_node_info(getter)
B.connect_pins(next(p.pin_id for p in ei.output_pins if p.name=='Started'),next(p.pin_id for p in ci.input_pins if p.type_id=='Exec'))
B.connect_pins(gi.output_pins[0].pin_id,next(p.pin_id for p in ci.input_pins if p.name=='self'))
B.compile_blueprint(child);unreal.EditorAssetLibrary.save_loaded_asset(child)
hud=unreal.load_asset(root+'/BP_InteractionHUD')
B.write_graph_dsl(B.get_graph(hud,'EventGraph'),'''(event AddEvent|EventReceiveDrawHUD (SizeX SizeY)
 (bind Pawn (HUD|GetOwningPawn))
 (Utilities|IsValid Pawn
  (:"Is Valid"
   (bind Component (Utilities|Casting|CastToBP_InteractionComponent :Object
     (Actor|GetComponentbyClass :self Pawn :ComponentClass "/Game/AIExample/Interaction/BP_InteractionComponent.BP_InteractionComponent_C"))
    (:then
     (HUD|DrawText
      :Text (Utilities|String|ToString(Text) (Class|BPInteractionComponent|GetPromptText :self Component))
      :TextColor "(R=1,G=1,B=1,A=1)" :ScreenX (- (* SizeX 0.5) 100.0) :ScreenY (* SizeY 0.7) :Scale 1.3))
    (:CastFailed)))
  (:"Is Not Valid")))''')
unreal.EditorAssetLibrary.save_loaded_asset(hud)
gm=unreal.load_asset(root+'/BP_InteractionTestGameMode')
unreal.get_default_object(gm.generated_class()).set_editor_property('hud_class',hud.generated_class())
unreal.EditorAssetLibrary.save_loaded_asset(gm)
level='/Game/AIExample/Maps/Lvl_InteractionTest'
if not unreal.EditorAssetLibrary.does_asset_exist(level):
    assert unreal.EditorAssetLibrary.duplicate_asset('/Game/AIExample/Maps/Lvl_CharacterTest',level)
ls=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert ls.load_level(level)
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
world.get_world_settings().set_editor_property('default_game_mode',gm.generated_class())
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
starts=[a for a in actors.get_all_level_actors() if isinstance(a,unreal.PlayerStart)]
for index,a in enumerate(starts):
    a.set_actor_location(unreal.Vector(-200,-100+index*160,100),False,True)
    a.set_actor_rotation(unreal.Rotator(0,0,0),False)
door=actors.spawn_actor_from_class(unreal.load_asset(root+'/BP_InteractionTestDoor').generated_class(),unreal.Vector(0,-60,0))
door.set_actor_label('Interaction Test Door')
assert ls.save_current_level()
print('INTERACTION_SETUP_READY',len(starts),'player starts')

