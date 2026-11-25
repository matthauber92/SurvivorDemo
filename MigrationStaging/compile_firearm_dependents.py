import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
for path in ['Items/BP_InventoryComponent','Interaction/BP_SurvivorInteractionCharacter','Items/BP_InventoryPlayerController','Interaction/BP_InteractionHUD','Items/BP_ItemPickup','UI/WBP_Inventory']:
 save(asset(path));print('COMPILED',path)
save(unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP'))
