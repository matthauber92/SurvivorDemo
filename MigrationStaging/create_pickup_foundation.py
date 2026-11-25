import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A
root='/Game/AIExample/Items'
at=unreal.AssetToolsHelpers.get_asset_tools()
def blueprint(name,parent):
    existing=unreal.load_asset(root+'/'+name)
    if existing:return existing
    f=unreal.BlueprintFactory();f.set_editor_property('parent_class',parent)
    return at.create_asset(name,root,unreal.Blueprint,f)
def var(bp,name,typ,array=False):
    if name not in B.list_variables(bp):
        if isinstance(typ,str):B.add_variable(bp,name,typ,container_type='ARRAY' if array else None)
        else:B.add_object_variable(bp,name,typ,container_type='ARRAY' if array else None)
definition=blueprint('PDA_ItemDefinition',unreal.PrimaryDataAsset)
for name,typ in [('ItemID','name'),('DisplayName','text'),('Description','text'),('Category','name'),('MaxStackSize','int'),('InventoryIcon',unreal.Texture2D.static_class()),('WorldMesh',unreal.StaticMesh.static_class())]:
    var(definition,name,typ)
    B.set_variable_instance_editable(definition,name,True)
B.compile_blueprint(definition);unreal.EditorAssetLibrary.save_loaded_asset(definition)
for name,itemid,title,desc,category,maxstack,mesh in [
 ('DA_HandgunAmmo','Ammo.Handgun','Handgun Ammo','A box of handgun ammunition.','Ammo',60,'Cube'),
 ('DA_FirstAidKit','Medical.FirstAidKit','First Aid Kit','Basic medical supplies.','Medical',5,'Cylinder'),
 ('DA_Key','Key.Placeholder','Key','A placeholder key for a future lock or puzzle.','Key',1,'Cone')]:
    asset=unreal.load_asset(root+'/'+name)
    if not asset:
        f=unreal.DataAssetFactory();f.set_editor_property('data_asset_class',definition.generated_class())
        asset=at.create_asset(name,root,unreal.DataAsset,f)
    for prop,value in {'ItemID':itemid,'DisplayName':unreal.Text(title),'Description':unreal.Text(desc),'Category':category,'MaxStackSize':maxstack,'WorldMesh':unreal.load_asset('/Engine/BasicShapes/'+mesh),'InventoryIcon':unreal.load_asset('/Engine/EngineResources/WhiteSquareTexture')}.items():asset.set_editor_property(prop,value)
    unreal.EditorAssetLibrary.save_loaded_asset(asset)
inventory=blueprint('BP_InventoryComponent',unreal.ActorComponent)
var(inventory,'ItemIDs','name',True);var(inventory,'Quantities','int',True);var(inventory,'MaximumSlots','int')
for n in ['ItemIDs','Quantities']:B.set_variable_replication(inventory,n,unreal.BlueprintVariableReplication.REPLICATED)
B.compile_blueprint(inventory)
icdo=unreal.get_default_object(inventory.generated_class());icdo.set_editor_property('replicates',True);icdo.set_editor_property('MaximumSlots',8)
unreal.EditorAssetLibrary.save_loaded_asset(inventory)
controller=blueprint('BP_InventoryPlayerController',unreal.PlayerController)
if not any(c.get_class()==inventory.generated_class() for c in A.get_components(unreal.get_default_object(controller.generated_class()))):A.add_component(controller,inventory.generated_class(),'InventoryComponent')
for c in A.get_components(unreal.get_default_object(controller.generated_class())):
    if c.get_class()==inventory.generated_class():c.set_editor_property('replicates',True)
B.compile_blueprint(controller);unreal.EditorAssetLibrary.save_loaded_asset(controller)
pickup=unreal.load_asset(root+'/BP_ItemPickup')
if not pickup:
    pickup=unreal.EditorAssetLibrary.duplicate_asset('/Game/AIExample/Interaction/BP_InteractionTestDoor',root+'/BP_ItemPickup')
    B.write_graph_dsl(B.get_graph(pickup,'EventGraph'),'')
    for gn in ['OnRep_IsOpen']:
        if B.get_graph(pickup,gn):B.remove_function_graph(pickup,gn)
    for name in list(B.list_variables(pickup)):
        if str(name) not in ['DefaultSceneRoot','DoorHinge','DoorPanel']:B.remove_variable(pickup,str(name))
    for c in list(A.get_components(unreal.get_default_object(pickup.generated_class()))):
        if c.get_name().startswith('DoorPanel'):A.remove_component(c)
    for c in list(A.get_components(unreal.get_default_object(pickup.generated_class()))):
        if c.get_name().startswith('DoorHinge'):A.remove_component(c)
    mesh=A.add_component(pickup,unreal.StaticMeshComponent.static_class(),'PickupMesh')
    mesh.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'))
    mesh.set_editor_property('relative_scale3d',unreal.Vector(.5,.5,.5))
    mesh.set_collision_profile_name('BlockAllDynamic')
var(pickup,'ItemDefinition',definition.generated_class());var(pickup,'Quantity','int');var(pickup,'Claimed','bool')
for n in ['ItemDefinition','Quantity']:B.set_variable_instance_editable(pickup,n,True)
B.compile_blueprint(pickup)
pcdo=unreal.get_default_object(pickup.generated_class());pcdo.set_editor_property('replicates',True);pcdo.set_editor_property('Quantity',1);pcdo.set_editor_property('ItemDefinition',unreal.load_asset(root+'/DA_HandgunAmmo'))
unreal.EditorAssetLibrary.save_loaded_asset(pickup)
gm=blueprint('BP_PickupTestGameMode',unreal.load_asset('/Game/AIExample/Interaction/BP_InteractionTestGameMode').generated_class())
B.compile_blueprint(gm);unreal.get_default_object(gm.generated_class()).set_editor_property('player_controller_class',controller.generated_class());unreal.EditorAssetLibrary.save_loaded_asset(gm)
report={}
for bp in [inventory,pickup]:
    g=B.get_graph(bp,'EventGraph')
    report[bp.get_name()]={term:list(B.find_node_types(g,term,[])) for term in ['Array|','GetItemID','GetMaxStackSize','GetDisplayName','GetWorldMesh','GetInventory','TryAdd','DestroyActor','GetComponentByClass','SetStaticMesh','GetPickupMesh','Min(Integer)','GetQuantity']}
(Path(unreal.Paths.project_saved_dir())/'PickupValidation/node-types.json').write_text(json.dumps(report,indent=2))
print('PICKUP_FOUNDATION_CREATED')

