import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
for path,names in [('Interaction/BP_SurvivorInteractionCharacter',['SetWeaponPresentation']),('Items/BP_InventoryComponent',['TryPistolAction','TryTransferWeapon','TrySelectWeapon'])]:
 bp=unreal.load_asset('/Game/AIExample/'+path)
 for name in names:
  print(name,B.read_graph_dsl(B.get_graph(bp,name))[:12000])
