import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
root='/Game/AIExample/Items/'
pickup=unreal.load_asset(root+'BP_ItemPickup')
B.set_variable_replication(pickup,'ItemDefinition',unreal.BlueprintVariableReplication.REP_NOTIFY)
B.set_variable_replication(pickup,'Quantity',unreal.BlueprintVariableReplication.REPLICATED)
B.write_graph_dsl(B.get_graph(pickup,'OnRep_ItemDefinition'),'''(fn OnRep_ItemDefinition ()
 (Utilities|IsValid (Variables|Default|GetItemDefinition)
  (:"Is Valid"
   (Components|StaticMesh|SetStaticMesh :self (Variables|Default|GetPickupMesh) :NewMesh (Class|PDAItemDefinition|GetWorldMesh :self (Variables|Default|GetItemDefinition))))
  (:"Is Not Valid")))''')
B.write_graph_dsl(B.get_graph(pickup,'EventGraph'),'''(event AddEvent|EventBeginPlay (CallFunction|OnRep_ItemDefinition))''')
B.compile_blueprint(pickup);unreal.EditorAssetLibrary.save_loaded_asset(pickup)
ls=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
level='/Game/AIExample/Maps/Lvl_PickupTest'
assert not unreal.EditorAssetLibrary.does_asset_exist(level),'Test level already exists; do not rebuild it blindly.'
assert ls.new_level(level)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
world.get_world_settings().set_editor_property('default_game_mode',unreal.load_asset(root+'BP_PickupTestGameMode').generated_class())
floor=actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(0,0,-50))
floor.set_actor_label('Pickup Test Floor');floor.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));floor.set_actor_scale3d(unreal.Vector(60,60,1));floor.static_mesh_component.set_collision_profile_name('BlockAll')
floor.static_mesh_component.set_material(0,unreal.load_asset('/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray'))
for i in range(14):
    a=actors.spawn_actor_from_class(unreal.PlayerStart,unreal.Vector(-450-(i//2)*150,-80+(i%2)*160,100))
    a.set_actor_label('Pickup PlayerStart %02d'%(i+1))
fixtures=[('Ammo_A','DA_HandgunAmmo',30,0,0),('Medkit_A','DA_FirstAidKit',1,0,300),('Key_A','DA_Key',1,0,-300),('Ammo_B','DA_HandgunAmmo',45,400,0),('Race_Item','DA_Key',1,400,300),('Capacity_Item','DA_FirstAidKit',1,400,-300)]
for label,definition,quantity,x,y in fixtures:
    a=actors.spawn_actor_from_class(pickup.generated_class(),unreal.Vector(x,y,100))
    a.set_actor_label(label)
    a.set_editor_property('ItemDefinition',unreal.load_asset(root+definition));a.set_editor_property('Quantity',quantity)
    a.call_method('UserConstructionScript')
door=actors.spawn_actor_from_class(unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionTestDoor').generated_class(),unreal.Vector(800,-60,0));door.set_actor_label('Regression Test Door')
light=actors.spawn_actor_from_class(unreal.DirectionalLight,unreal.Vector(0,0,1000),unreal.Rotator(pitch=-45,yaw=30,roll=0))
light.light_component.set_editor_property('mobility',unreal.ComponentMobility.MOVABLE);light.light_component.set_editor_property('intensity',10)
actors.spawn_actor_from_class(unreal.SkyAtmosphere,unreal.Vector())
sky=actors.spawn_actor_from_class(unreal.SkyLight,unreal.Vector(0,0,500));sky.light_component.set_editor_property('mobility',unreal.ComponentMobility.MOVABLE);sky.light_component.set_editor_property('real_time_capture',False);sky.light_component.recapture_sky()
assert ls.save_current_level()
print('PICKUP_LEVEL_READY',len(fixtures),'pickups, 14 starts, existing door')
