import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
b=unreal.load_asset('/Game/AIExample/Items/BP_ItemPickup');print(B.read_graph_dsl(B.get_graph(b,'ApplyDefinitionMesh')))
for w in unreal.EditorLevelLibrary.get_pie_worlds(False):
 for a in unreal.GameplayStatics.get_all_actors_of_class(w,b.generated_class()):
  if str(a.get_editor_property('ItemDefinition').get_editor_property('ItemID'))=='Weapon.Pistol':
   print(w.get_name(),a.get_name(),[(k,str(a.get_editor_property(k))) for k in ['replicates','replicate_movement','net_dormancy','net_update_frequency','root_component']],a.get_editor_property('PickupMesh').is_simulating_physics())
