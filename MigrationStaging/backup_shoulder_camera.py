from pathlib import Path
import shutil,datetime
root=Path(__file__).resolve().parent.parent
dest=root/'Backups'/('BeforeShoulderCamera-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
for rel in ['Content/AIExample/Interaction/BP_SurvivorInteractionCharacter.uasset','Content/AIExample/Interaction/BP_InteractionHUD.uasset','Content/AIExample/Items/BP_InventoryPlayerController.uasset','Content/AIExample/Items/BP_InventoryComponent.uasset']:
 d=dest/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/rel,d)
print(dest)
