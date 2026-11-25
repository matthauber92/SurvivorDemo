import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionComponent')
print('REQUEST',B.read_graph_dsl(B.get_graph(bp,'RequestInteraction')))
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
    p=unreal.GameplayStatics.get_player_pawn(w,0)
    c=p.get_component_by_class(bp.generated_class())
    d=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionTestDoor.BP_InteractionTestDoor_C'))[0]
    print('COMP',p.has_authority(),c.get_editor_property('replicates'))
    if not p.has_authority():
        c.call_method('ServerInteract',(d,unreal.Vector(-480,0,100.15),unreal.Vector(1,0,0)))
        print('RPC_DIRECT')
    for other in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Pawn):
        if other.has_authority() and not other.is_locally_controlled():
            oc=other.get_component_by_class(bp.generated_class())
            print('SERVER_OWNER',oc.get_editor_property('OwnerPawn'))
            oc.call_method('ServerInteract',(d,unreal.Vector(-480,0,100.15),unreal.Vector(1,0,0)))
            print('SERVER_EVENT_RESULT',d.get_editor_property('IsOpen'))
print('FUNCTION_GRAPHS',B.list_graphs(bp))
