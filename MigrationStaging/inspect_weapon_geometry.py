import unreal,json
from pathlib import Path
out={}
for name in ['Revolver','Shotgun']:
 mesh=unreal.load_asset('/Game/AIExample/Weapons/TheHouse/04_Weapons/'+name+'/Mesh/SM_'+name)
 dm,ok=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(mesh,unreal.DynamicMesh(),unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD())
 result=dm.get_all_vertex_positions(False)
 vs=result[1].convert_vector_list_to_array()
 out[name]=[[v.x,v.y,v.z] for v in vs]
(Path(unreal.Paths.project_saved_dir())/'weapon-vertices.json').write_text(json.dumps(out))
