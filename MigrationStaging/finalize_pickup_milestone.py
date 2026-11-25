import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A
root='/Game/AIExample/Items/'
folder=Path(unreal.Paths.project_saved_dir())/'PickupValidation'
compiled={}
for name in ['PDA_ItemDefinition','BP_InventoryComponent','BP_InventoryPlayerController','BP_ItemPickup','BP_PickupTestGameMode']:
    bp=unreal.load_asset(root+name)
    B.compile_blueprint(bp)
    compiled[name]=str(bp.get_editor_property('status'))
    assert 'BS_UP_TO_DATE' in compiled[name],(name,compiled[name])
    unreal.EditorAssetLibrary.save_loaded_asset(bp)
    (folder/(name+'-graphs.json')).write_text(json.dumps({g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(bp)},indent=2))
definitions=[]
for name in ['DA_HandgunAmmo','DA_FirstAidKit','DA_Key']:
    d=unreal.load_asset(root+name)
    item={p:str(d.get_editor_property(p)) for p in ['ItemID','DisplayName','Description','Category']}
    item['MaxStackSize']=d.get_editor_property('MaxStackSize')
    item['InventoryIcon']=d.get_editor_property('InventoryIcon').get_path_name()
    item['WorldMesh']=d.get_editor_property('WorldMesh').get_path_name()
    assert item['MaxStackSize']>0
    unreal.EditorAssetLibrary.save_loaded_asset(d);definitions.append(item)
assert len({d['ItemID'] for d in definitions})==3
pc=unreal.load_asset(root+'BP_InventoryPlayerController')
inventory=unreal.load_asset(root+'BP_InventoryComponent')
assert all(c.get_editor_property('replicates') for c in A.get_components(unreal.get_default_object(pc.generated_class())) if c.get_class()==inventory.generated_class())
assert unreal.get_default_object(inventory.generated_class()).get_editor_property('MaximumSlots')==8
pickup=unreal.load_asset(root+'BP_ItemPickup')
assert unreal.SystemLibrary.does_implement_interface(unreal.get_default_object(pickup.generated_class()),unreal.load_asset('/Game/AIExample/Interaction/BPI_Interactable').generated_class())
assert 'SetClaimed' in B.read_graph_dsl(B.get_graph(pickup,'TryInteract'))
assert 'DestroyActor' in B.read_graph_dsl(B.get_graph(pickup,'TryInteract'))
assert 'LoadAsset' in B.read_graph_dsl(B.get_graph(pickup,'OnRep_DefinitionPath'))
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name()=='Lvl_PickupTest'
assert len([a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors() if isinstance(a,unreal.PlayerStart)])==14
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
tests={name:json.loads((folder/(name+'-result.json')).read_text()) for name in ['singleplayer','multiplayer','keyboard']}
assert all(t['passed'] for t in tests.values())
report={
 'milestone':3,'status':'implemented and tested','level':'/Game/AIExample/Maps/Lvl_PickupTest',
 'blueprint_compilation':compiled,'item_definitions':definitions,
 'architecture':{
  'interaction':'Existing BPI_Interactable, BP_InteractionComponent, ServerInteract RPC, E mapping, focus prompt and target validation are reused.',
  'inventory_owner':'BP_InventoryComponent is attached to BP_InventoryPlayerController. PlayerController relevance confines inventory replication to its owning client; the server holds every player inventory.',
  'storage':'Eight stack slots. ItemIDs (Name array) and Quantities (integer array) use matching indices. Definitions remain separate and immutable during collection. GetItemQuantity is the read API; TryAddItem is the server-only mutation API.',
  'capacity':'Existing partial stacks are filled first, then new slots. CanAddItem preflights the complete amount; insufficient capacity rejects the entire pickup without partial insertion.',
  'definition_replication':'The pickup replicates a SoftObjectPath, resolves its Primary Data Asset locally, and updates its primitive mesh. Quantity also replicates. No definition object is used as a replicated mutable inventory instance.',
  'race_handling':'The authoritative pickup sets Claimed before synchronous insertion. Failure releases the claim; success destroys the replicated actor. No latent steps occur in the transaction.',
  'integration':'BP_PickupTestGameMode inherits the existing interaction game mode, uses the existing survivor character and HUD, and adds only the inventory controller.',
  'future':'Stack indices, item IDs, and quantities are available to future server operations. Dropping, splitting, equipping, consuming, reloading, puzzle logic, persistence and inventory UI are not implemented.'},
 'tests':tests,
 'manual_testing_remaining':['14-player load and contention (host plus 13 clients)','Separate-process/packaged multiplayer and real network latency, packet loss, and late joins','Human playthrough and visual review of placeholder meshes, prompt placement and movement around pickups'],
 'notes':['The existing DefaultGame.ini MaxPlayers=14 setting is preserved. The new map has 14 PlayerStarts.','Three definitions use built-in cube/cylinder/cone meshes and a white-square placeholder inventory icon.','The authoritative same-frame contention test uses two TryInteract calls against one pickup; it is not a 14-client network stress test.','Automated play tests inject the existing Enhanced Input action; the separate keyboard test uses real Windows E keydown/keyup in the client viewport.']}
(folder/'milestone3-report.json').write_text(json.dumps(report,indent=2))
print('MILESTONE3_VALIDATED',len(compiled),'Blueprints,',sum(len(t['checks']) for t in tests.values()),'checks')
