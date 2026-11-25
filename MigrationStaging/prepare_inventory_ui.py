import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B, ContainerType
R='/Game/AIExample/';ui=unreal.load_asset(R+'UI/WBP_Inventory');pc=unreal.load_asset(R+'Items/BP_InventoryPlayerController');inv=unreal.load_asset(R+'Items/BP_InventoryComponent')
out=Path(unreal.Paths.project_saved_dir())/'InventoryUIValidation';out.mkdir(exist_ok=True)
# Backup original graphs before any inventory/controller changes.
for b in [pc,inv]:
 p=out/(b.get_name()+'-before.json')
 if not p.exists():p.write_text(json.dumps({g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(b)},indent=2))
def var(b,n,t,array=False):
 if n not in B.list_variables(b):
  if isinstance(t,str):B.add_variable(b,n,t,container_type=ContainerType.ARRAY if array else None)
  else:B.add_object_variable(b,n,t,container_type=ContainerType.ARRAY if array else None)
def fn(b,n):return B.get_graph(b,n) or B.add_function_graph(b,n)
var(pc,'InventoryWidget',ui.generated_class());var(pc,'InventoryOpen','bool')
for n in ['ToggleInventory','CloseInventory','RefreshInventory']:fn(pc,n)
var(ui,'InventorySource',inv.generated_class());var(ui,'ItemCatalog',unreal.load_asset(R+'Items/PDA_ItemDefinition').generated_class(),True)
var(ui,'ResolvedName','text');var(ui,'ResolvedIcon',unreal.Texture2D.static_class());var(ui,'OccupiedLabel',unreal.TextBlock.static_class())
for n,t in [('NameLabels',unreal.TextBlock),('QuantityLabels',unreal.TextBlock),('IconFrames',unreal.Border)]:var(ui,n,t.static_class(),True)
fn(ui,'RefreshInventory');fn(ui,'CacheSlotWidgets')
for b in [pc,ui]:B.compile_blueprint(b)
unreal.get_default_object(ui.generated_class()).set_editor_property('ItemCatalog',[unreal.load_asset(R+'Items/'+n) for n in ['DA_HandgunAmmo','DA_FirstAidKit','DA_Key']])
f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',unreal.InputAction)
a=unreal.load_asset(R+'UI/IA_ToggleInventory') or unreal.AssetToolsHelpers.get_asset_tools().create_asset('IA_ToggleInventory',R+'UI',unreal.InputAction,f)
a.set_editor_property('value_type',unreal.InputActionValueType.BOOLEAN)
c=unreal.load_asset(R+'Interaction/IMC_SurvivorInteraction');c.unmap_all_keys_from_action(a);k=unreal.Key();k.import_text('I');c.map_key(a,k)
for obj in [a,c]:unreal.EditorAssetLibrary.save_loaded_asset(obj)
g=B.get_graph(ui,'EventGraph')
terms=['ToText','Append','IsValidIndex','SetRenderOpacity','SetVisibility','GetInputEventfromKeyEvent','Equal','IA_ToggleInventory','RefreshInventory','CloseInventory']
report={term:list(B.find_node_types(g,term,[])) for term in terms}
(out/'node-types.json').write_text(json.dumps(report,indent=2))
for term in ['Widget|Panel|GetContent','Widget|Panel|GetChildAt','Input|KeyEvent|GetKey','Input|InputEvent|IsRepeat','Input|SetInputModeUIOnly']:
 print(term,[(p.name,p.type_id) for p in B.get_node_type_pins(g,term).input_pins])
print('CREATED')


