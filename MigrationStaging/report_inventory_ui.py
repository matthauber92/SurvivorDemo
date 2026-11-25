import json
from pathlib import Path
out=Path('Saved/InventoryUIValidation')
report={
 'milestone':4,
 'assets':{'widget':'/Game/AIExample/UI/WBP_Inventory','input_action':'/Game/AIExample/UI/IA_ToggleInventory','mapping_context':'/Game/AIExample/Interaction/IMC_SurvivorInteraction','controller':'/Game/AIExample/Items/BP_InventoryPlayerController','inventory':'/Game/AIExample/Items/BP_InventoryComponent'},
 'implementation':[
  'Four columns by two rows, dark palette, item icon/placeholder, item name, stack quantity, explicit empty slots, and occupied count.',
  'I is mapped through Enhanced Input and Started opens the screen. The focused widget handles I and Escape, ignores key repeat, and returns Unhandled for other keys.',
  'The local PlayerController creates the widget with itself as owning player and uses AddToPlayerScreen. UI-only input and balanced move/look ignore flags prevent accidental gameplay input while browsing.',
  'Closing hides the cursor, restores GameOnly input and game viewport focus/capture, and removes the screen. No game pause or time dilation is used.',
  'Reuses ItemIDs and Quantities from the existing owner-relevant PlayerController inventory. No duplicate inventory store or UI RPCs.',
  'RepNotify on both existing arrays refreshes the owning client. The authoritative TryAddItem success path notifies the local host after the transaction completes. UI reads only matching valid indices.',
  'Names and icons resolve from a local catalog of the three existing item definitions; unknown IDs retain an ID label and fallback icon. The current definitions use white-square placeholder icons.',
  'InventoryWidget and InventoryOpen are non-replicated. MaxPlayers remains 14, including host.',
  'Opening is skipped if another cursor-based menu already owns input. Escape is handled only by the focused inventory widget; there is no global Escape binding.'
 ],
 'validation':{},
 'manual_checks_remaining':['14-player load test (host plus 13 clients).','Packaged multiplayer, network latency/loss, late joins, and human visual review at other display sizes.'],
 'scope':'No Git initialization, Lyra, item use, dropping, equipment, or crafting.'
}
for name in ['standalone','multiplayer']:
 report['validation'][name]=json.loads((out/(name+'-result.json')).read_text())
report['validation']['pickup_regression']=json.loads(Path('Saved/PickupValidation/multiplayer-result.json').read_text())
report['validation']['blueprints']=json.loads((out/'blueprint-validation.json').read_text())
(out/'milestone4-report.json').write_text(json.dumps(report,indent=2))
print('REPORT_WRITTEN')
