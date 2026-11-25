import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);a=p.mesh.get_anim_instance()
print('STATE',[(n,str(p.get_editor_property(n))) for n in ['PublicActiveSlot','PublicSidearm','PublicAiming','PistolPoseUntil']])
print('ANIM',a.get_path_name(),a.try_get_pawn_owner()==p)
p.call_method('NoteHipFire');print('TIME',unreal.GameplayStatics.get_time_seconds(w),p.get_editor_property('PistolPoseUntil'))
a.call_method('UpdatePistolLayer',(1.0,));print('WEIGHT',a.get_editor_property('PistolLayerWeight'))
print(B.read_graph_dsl(B.get_graph(unreal.load_asset('/Game/AIExample/Combat/Animation/ABP_SurvivorCombat'),'UpdatePistolLayer')))
