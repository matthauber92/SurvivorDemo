import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
root='/Game/AIExample/Items/'
bp=unreal.load_asset(root+'BP_ItemPickup')
iface=unreal.load_asset('/Game/AIExample/Interaction/BPI_Interactable')
assert unreal.SystemLibrary.does_implement_interface(unreal.get_default_object(bp.generated_class()),iface.generated_class())
g=B.get_graph(bp,'GetInteractionPrompt')
for term in ['Append','TryAddItem','CanAddItem','CastToBP_InventoryComponent']:
    print('TYPES',term,[t for t in B.find_node_types(g,term,[]) if 'String' in t or term!='Append'])
def write(name,code):
    g=B.get_graph(bp,name)
    B.write_graph_dsl(g,code)
    actual=B.read_graph_dsl(g)
    assert len(actual)>100,(name,actual)
    print(name,actual)
write('GetInteractionPrompt','''(fn GetInteractionPrompt (Interactor)
 (Utilities|IsValid (Variables|Default|GetItemDefinition)
  (:"Is Valid"
   (Utilities|IsValid Interactor
    (:"Is Valid"
     (bind Inventory (Utilities|Casting|CastToBP_InventoryComponent :Object
       (Actor|GetComponentbyClass :self (Pawn|GetController :self Interactor) :ComponentClass "/Game/AIExample/Items/BP_InventoryComponent.BP_InventoryComponent_C"))
      (:then
       (if (Class|BPInventoryComponent|CanAddItem :self Inventory :Definition (Variables|Default|GetItemDefinition) :Amount (Variables|Default|GetQuantity))
        (return (Utilities|String|Append "Press E to collect " (Utilities|String|ToString(Text) (Class|PDAItemDefinition|GetDisplayName :self (Variables|Default|GetItemDefinition)))))
        (else (return "Inventory full"))))
      (:CastFailed (return "Inventory unavailable"))))
    (:"Is Not Valid" (return ""))))
  (:"Is Not Valid" (return ""))))''')
write('TryInteract','''(fn TryInteract (Interactor)
 (if (Networking|HasAuthority)
  (if (not (Variables|Default|GetClaimed))
   (Utilities|IsValid Interactor
    (:"Is Valid"
     (if (<= (Math|Vector|VectorLength (- (Transformation|GetActorLocation :self Interactor) (Transformation|GetActorLocation))) 250.0)
      (bind Inventory (Utilities|Casting|CastToBP_InventoryComponent :Object
       (Actor|GetComponentbyClass :self (Pawn|GetController :self Interactor) :ComponentClass "/Game/AIExample/Items/BP_InventoryComponent.BP_InventoryComponent_C"))
       (:then
        (Variables|Default|SetClaimed true)
        (if (Class|BPInventoryComponent|TryAddItem :self Inventory :Definition (Variables|Default|GetItemDefinition) :Amount (Variables|Default|GetQuantity))
         (Actor|DestroyActor)
         (return true)
         (else
          (Variables|Default|SetClaimed false)
          (return false))))
       (:CastFailed (return false)))
      (else (return false))))
    (:"Is Not Valid" (return false)))
   (else (return false)))
  (else (return false))))''')
write('UserConstructionScript','''(fn ConstructionScript ()
 (Utilities|IsValid (Variables|Default|GetItemDefinition)
  (:"Is Valid"
   (Components|StaticMesh|SetStaticMesh :self (Variables|Default|GetPickupMesh) :NewMesh (Class|PDAItemDefinition|GetWorldMesh :self (Variables|Default|GetItemDefinition))))
  (:"Is Not Valid")))''')
B.compile_blueprint(bp)
assert 'BS_UP_TO_DATE' in str(bp.get_editor_property('status'))
unreal.EditorAssetLibrary.save_loaded_asset(bp)
print('PICKUP_LOGIC_SAVED')

