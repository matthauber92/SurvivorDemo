import unreal,uuid
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionComponent')
g=B.get_graph(bp,'EventGraph')
for n in B.find_nodes(g):
    if isinstance(n,unreal.K2Node_CustomEvent):B.delete_node(n)
lines=['Begin Object Class=/Script/BlueprintGraph.K2Node_CustomEvent Name="K2Node_CustomEvent_Interaction"',' CustomFunctionName="ServerInteract"',' FunctionFlags=203555008',' NodePosX=600',' NodePosY=200',' NodeGuid='+uuid.uuid4().hex.upper()]
for name,cat,sub in [('then','exec',''),('Target','object','/Script/Engine.Actor'),('ViewOrigin','struct','/Script/CoreUObject.Vector'),('ViewDirection','struct','/Script/CoreUObject.Vector')]:
    obj='None' if not sub else '"'+('/Script/CoreUObject.Class' if cat=='object' else '/Script/CoreUObject.ScriptStruct')+"'"+sub+"'\""
    lines.append(' CustomProperties Pin (PinId='+uuid.uuid4().hex.upper()+',PinName="'+name+'",Direction="EGPD_Output",PinType.PinCategory="'+cat+'",PinType.PinSubCategoryObject='+obj+',)')
    if cat!='exec':lines.append(' CustomProperties UserDefinedPin (PinName="'+name+'",PinType=(PinCategory="'+cat+'",PinSubCategoryObject='+obj+'),DesiredPinDirection=EGPD_Output)')
lines.append('End Object')
(Path(unreal.Paths.project_dir())/'MigrationStaging/interaction-rpc-node.txt').write_text('\n'.join(lines))
print('Prepared RPC node')
