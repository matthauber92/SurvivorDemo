import unreal
R='/Game/AIExample/';sub=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for name in ['DA_RevolverItem','DA_ShotgunItem','DA_RevolverAmmo','DA_ShotgunAmmo','DA_HandgunAmmo']:
 m=unreal.load_asset(R+'Items/'+name).get_editor_property('WorldMesh');print(name,'BEFORE',sub.get_simple_collision_count(m),sub.get_convex_collision_count(m))
 body=m.get_editor_property('body_setup');print('COMPLEXITY',body.get_editor_property('collision_trace_flag'))
 body.set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_SIMPLE_AND_COMPLEX)
 if sub.get_simple_collision_count(m)==0 and sub.get_convex_collision_count(m)==0:assert sub.add_simple_collisions(m,unreal.ScriptCollisionShapeType.NDOP26)>=0
 unreal.EditorAssetLibrary.save_loaded_asset(m,False)
print('PICKUP_COLLISION_READY')
