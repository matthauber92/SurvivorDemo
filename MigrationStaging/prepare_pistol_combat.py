import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'MigrationStaging'))
from combat_helpers import *
char=asset('Interaction/BP_SurvivorInteractionCharacter');inv=asset('Items/BP_InventoryComponent')
with toolset_registry.tool_raising_exceptions():
 for n,t,rep in [('PublicAiming','bool',True),('PublicReloading','bool',True),('PublicShotSerial','int',True),('PublicImpactLocation','Vector',False),('PublicHasImpact','bool',False)]:
  var(char,n,t,rep)
  if not rep:B.set_variable_replication(char,n,unreal.BlueprintVariableReplication.REPLICATED)
 for n,t,rep in [('Reloading','bool',True),('ReloadInstance','string',False),('ReloadEndTime','float',False),('NextFireTime','float',False),('DryFireSerial','int',True)]:var(inv,n,t,rep)
 # Create presentation entry points before inventory refers to them.
 for n,ins in [('PerformPistolShot',[('ViewOrigin','Vector'),('ViewDirection','Vector')]),('PlayPistolShot',[]),('RefreshPistolReload',[]),('RefreshPistolAim',[])]:fn(char,n,ins)
 save(char);save(inv)
 g=B.get_graph(char,'EventGraph')
 for term in ['PlaySlotAnimation','GetAnimInstance','SpawnSystemAttached','SpawnSystemAtLocation','PlaySoundAtLocation','ApplyPointDamage','SetAnimInstanceClass','GetActorEyes','GetBaseAim','GetWorldLocation','SetFieldOfView']:
  print('COMBAT_TYPES',term,[x for x in B.find_node_types(g,term,[]) if 'Casting' not in x][:10])
 abp=unreal.load_asset('/Game/Blueprints/SandboxCharacter_CMC_ABP');ag=B.get_graph(abp,'AnimGraph')
 print('LAYER_TYPES',[x for x in B.find_node_types(ag,'Layered',[]) if x.startswith('Animation|')])
 for nm in ['Survivor_MF_Pistol_Idle_ADS','Survivor_MM_Pistol_Fire','Survivor_MM_Pistol_Reload','Survivor_AO_Pistol']:
  a=asset('Combat/Animation/'+nm)
  print('ANIM_DETAIL',nm,a.get_editor_property('skeleton').get_name(),str(a.get_editor_property('additive_anim_type')) if isinstance(a,unreal.AnimSequence) else '')
