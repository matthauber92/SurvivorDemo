import unreal,ast,toolset_registry
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A
R='/Game/AIExample/'
with toolset_registry.tool_raising_exceptions():
 bp=unreal.load_asset(R+'Items/BP_ItemPickup')
 c=next((c for c in A.get_components(unreal.get_default_object(bp.generated_class())) if 'WeaponInteractionTarget' in c.get_name()),None)
 if not c:c=A.add_component(bp,unreal.SphereComponent.static_class(),'WeaponInteractionTarget')
 c.set_sphere_radius(32,False)
 c.set_collision_profile_name('Custom')
 c.set_editor_property('relative_scale3d',unreal.Vector(1,1,1))
 c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
 c.set_collision_response_to_all_channels(unreal.CollisionResponseType.ECR_IGNORE)
 c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_BLOCK)
 c.set_editor_property('generate_overlap_events',False)
 c.set_editor_property('can_ever_affect_navigation',False)
 c.set_editor_property('can_character_step_up_on',unreal.CanBeCharacterBase.ECB_NO)
 c.set_editor_property('hidden_in_game',True)
 c.set_editor_property('absolute_scale',True)
 B.compile_blueprint(bp)
 source=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/fix_pickup_physics.py').read_text())
 code=next(ast.literal_eval(n.value) for n in source.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='code' for t in n.targets))
 code=code.replace('(fn ApplyDefinitionMesh ()','''(fn ApplyDefinitionMesh ()
 (Transformation|SetWorldScale3D :self (Variables|Default|GetWeaponInteractionTarget) :NewScale "1,1,1")
 (Collision|SetCollisionEnabled :self (Variables|Default|GetWeaponInteractionTarget) :NewType "NoCollision")
 (Collision|SetCollisionResponsetoAllChannels :self (Variables|Default|GetWeaponInteractionTarget) :NewResponse "ECR_Ignore")
 (Collision|SetCollisionResponsetoChannel :self (Variables|Default|GetWeaponInteractionTarget) :Channel "ECC_Visibility" :NewResponse "ECR_Block")''')
 code=code.replace('(Networking|SetReplicateMovement','''(Collision|SetCollisionResponsetoChannel :self (Variables|Default|GetPickupMesh) :Channel "ECC_Pawn" :NewResponse "ECR_Ignore")
     (Collision|SetCollisionResponsetoChannel :self (Variables|Default|GetPickupMesh) :Channel "ECC_Camera" :NewResponse "ECR_Ignore")
     (Collision|SetCollisionEnabled :self (Variables|Default|GetWeaponInteractionTarget) :NewType "QueryOnly")
     (Networking|SetReplicateMovement''')
 B.write_graph_dsl(B.get_graph(bp,'ApplyDefinitionMesh'),code)
 B.compile_blueprint(bp,warnings_as_errors=True)
 assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 char=unreal.load_asset(R+'Interaction/BP_SurvivorInteractionCharacter')
 src=ast.parse((Path(unreal.Paths.project_dir())/'MigrationStaging/build_weapon_switching.py').read_text())
 code=next(ast.literal_eval(n.args[2]) for n in ast.walk(src) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='write' and isinstance(n.args[1],ast.Constant) and n.args[1].value=='UpdateWeaponVisual')
 # Put the grip in the palm rather than over the wrist. Turn the holstered
 # pistol flat against the outside of the thigh, with its muzzle downward.
 code=code.replace(':Location "-4,0,5" :Rotation "0,180,0"',':Location "-13,2,3" :Rotation "0,180,0"')
 code=code.replace(':Location "-5,-2,18" :Rotation "0,180,0"',':Location "-5,-2,18" :Rotation (Math|Rotator|MakeRotator :Pitch 0 :Yaw 180 :Roll -90)')
 # Leave the long-gun placeholder transform as before.
 old='(Transformation|SetRelativeTransform :self Visual :NewTransform (Math|Transform|MakeTransform :Location "-13,2,3" :Rotation "0,180,0" :Scale "1,1,1"))'
 code=code.replace(old,'(if (== ID "Weapon.Pistol") '+old+' (else (Transformation|SetRelativeTransform :self Visual :NewTransform (Math|Transform|MakeTransform :Location "-4,0,5" :Rotation "0,180,0" :Scale "1,1,1"))))')
 B.write_graph_dsl(B.get_graph(char,'UpdateWeaponVisual'),code)
 B.compile_blueprint(char,warnings_as_errors=True)
 assert unreal.EditorAssetLibrary.save_loaded_asset(char,only_if_is_dirty=False)
 print('PISTOL_GRIP_AND_INTERACTION_TARGET_SAVED')



