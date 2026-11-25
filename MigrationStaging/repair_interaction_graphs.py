import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
root='/Game/AIExample/Interaction'
door=unreal.load_asset(root+'/BP_InteractionTestDoor')
print('Interface funcs',[str(f) for f in B.list_functions(door) if 'Interact' in str(f.name)])
for name in ['GetInteractionPrompt','TryInteract']: B.add_function_graph(door,name)
g=B.get_graph(door,'EventGraph')
print('Hinge',list(B.find_node_types(g,'GetDoorHinge',[])))
comp=unreal.load_asset(root+'/BP_InteractionComponent')
cg=B.get_graph(comp,'UpdateFocus')
for n in B.find_nodes(cg):
    i=B._get_node_info(n)
    if 'vector*' in i.type_id or 'CameraManager' in i.type_id:print(i)
hud=unreal.load_asset(root+'/BP_InteractionHUD')
hg=B.get_graph(hud,'EventGraph')
print('HUD events',[str(e) for e in B.list_events(hud) if 'Draw' in str(e.name)])
for term in ['DrawText','GetOwningPawn','CastToBP_InteractionComponent']:
    for t in B.find_node_types(hg,term,[]):
        if t in ['HUD|DrawText','HUD|GetOwningPawn','Utilities|Casting|CastToBP_InteractionComponent']:print(B.get_node_type_pins(hg,t))

