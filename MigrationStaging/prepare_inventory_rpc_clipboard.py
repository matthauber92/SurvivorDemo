import uuid
from pathlib import Path
lines=['Begin Object Class=/Script/BlueprintGraph.K2Node_CustomEvent Name="K2Node_CustomEvent_InventoryMove"',' CustomFunctionName="ServerMoveInventory"',' FunctionFlags=203555008',' NodePosX=0',' NodePosY=1200',' NodeGuid='+uuid.uuid4().hex.upper()]
for name,cat in [('then','exec'),('SourceSlot','int'),('TargetSlot','int'),('ExpectedID','name'),('ExpectedQuantity','int'),('ExpectedLayoutVersion','int')]:
 lines.append(' CustomProperties Pin (PinId='+uuid.uuid4().hex.upper()+',PinName="'+name+'",Direction="EGPD_Output",PinType.PinCategory="'+cat+'",PinType.PinSubCategoryObject=None,)')
 if cat!='exec':lines.append(' CustomProperties UserDefinedPin (PinName="'+name+'",PinType=(PinCategory="'+cat+'"),DesiredPinDirection=EGPD_Output)')
lines.append('End Object');Path('MigrationStaging/inventory-rpc-node.txt').write_text('\n'.join(lines))
