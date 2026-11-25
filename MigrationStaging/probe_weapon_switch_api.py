import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
char=unreal.load_asset('/Game/AIExample/Interaction/BP_SurvivorInteractionCharacter');g=B.get_graph(char,'EventGraph')
for node in ['Transformation|AttachComponentToComponent','Transformation|SetRelativeTransform','Development|SetHiddeninGame','Pawn|GetControlledPawn']:
 print('PINS',node,B.get_node_type_pins(g,node))
pc=unreal.load_asset('/Game/AIExample/Items/BP_InventoryPlayerController');pg=B.get_graph(pc,'EventGraph')
for term in ['GetControlledPawn','Possess','GetTime','GetMesh']:print(term,list(B.find_node_types(pg,term,[]))[:12])
reg=unreal.AssetRegistryHelpers.get_asset_registry()
for ad in reg.get_assets_by_class(unreal.TopLevelAssetPath('/Script/EnhancedInput','InputMappingContext'),True):
 if not str(ad.package_name).startswith('/Game/'):continue
 for m in ad.get_asset().get_editor_property('default_key_mappings').get_editor_property('mappings'):
  if m.get_editor_property('key').export_text() in ['One','Two','Three','1','2','3']:
   print('KEY_CONFLICT',ad.package_name,m.export_text())
