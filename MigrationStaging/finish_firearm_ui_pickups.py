import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from weapon_extension_helpers import *
hud=asset('Interaction/BP_InteractionHUD')
code=code_from('build_pistol_hud_target.py','DrawPistolHUD').replace(':ItemID "Ammo.Handgun"',':ItemID (Class|BPInventoryComponent|GetActiveAmmoID :self Inventory)').replace('"PISTOL  "','(select (== (Class|BPInventoryComponent|GetActiveWeaponID :self Inventory) "Weapon.Shotgun") "SHOTGUN  " (select (== (Class|BPInventoryComponent|GetActiveWeaponID :self Inventory) "Weapon.Revolver") "REVOLVER  " "PISTOL  "))').replace('3 Holster','1/2/3 Draw or holster')
first=code.index('   (HUD|DrawLine');code=code[:first]+'''   (bind Pawn (Utilities|Casting|CastToBP_SurvivorInteractionCharacter (Pawn|GetControlledPawn :self PC)))
   (if (Class|BPSurvivorInteractionCharacter|GetShouldShowCrosshair :self Pawn)
'''+code[first:]+')'
write(hud,'DrawPistolHUD',code);save(hud)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);allactors=actors.get_all_level_actors();existing={a.get_actor_label() for a in allactors}
reference=next((a for a in allactors if a.get_class()==asset('Items/BP_ItemPickup').generated_class() and str(a.get_editor_property('ItemDefinition').get_editor_property('ItemID'))=='Weapon.Pistol'),None)
origin=reference.get_actor_location() if reference else unreal.Vector(0,300,100)
print('PICKUP_REFERENCE',reference,origin)
for name,offset,amount in [('DA_RevolverItem',unreal.Vector(0,100,25),1),('DA_ShotgunItem',unreal.Vector(0,200,25),1),('DA_RevolverAmmo',unreal.Vector(80,100,25),24),('DA_ShotgunAmmo',unreal.Vector(80,200,25),16)]:
 label='FirearmPickup_'+name
 a=next((a for a in allactors if a.get_actor_label()==label),None) or actors.spawn_actor_from_class(asset('Items/BP_ItemPickup').generated_class(),origin+offset);a.set_actor_label(label)
 a.set_actor_location(origin+offset,False,True)
 for k,v in [('ItemDefinition',asset('Items/'+name)),('Quantity',amount)]:a.set_editor_property(k,v)
 a.call_method('ApplyDefinitionMesh')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
print('NIAGARA_API',[n for n in dir(unreal.NiagaraSystem) if any(x in n for x in ['emitter','parameter','compile'])])
