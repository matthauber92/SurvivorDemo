import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from weapon_extension_helpers import *
bp=asset('Interaction/BP_SurvivorInteractionCharacter')
write(bp,'InitializePistolAnimation','''(fn InitializePistolAnimation () (Components|SkeletalMesh|SetAnimInstanceClass :self (Variables|Character|GetMesh) :NewClass "/Game/Blueprints/SandboxCharacter_CMC_ABP.SandboxCharacter_CMC_ABP_C"))''')
B.get_default_object(bp).mesh.set_editor_property('anim_class',unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP').generated_class());save(bp)
print('ACTIVE_COMBAT_ANIM_FIXED')
