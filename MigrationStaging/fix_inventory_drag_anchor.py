import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B

bp = unreal.load_asset('/Game/AIExample/UI/WBP_Inventory')
graph = B.get_graph(bp, 'OnDragDetected')
nodes = [B._get_node_info(n) for n in B.find_nodes(graph)]
node = next(n for n in nodes if 'CreateDrag' in n.type_id)
pin = next(p for p in node.input_pins if p.name == 'Pivot')
# MouseDown is relative to the entire inventory widget, not the clicked slot.
# Center anchors the small drag visual directly to the cursor.
B.set_pin_value(pin.pin_id, 'CenterCenter')
B.compile_blueprint(bp, warnings_as_errors=True)
assert bp.get_editor_property('status') == unreal.BlueprintStatus.BS_UP_TO_DATE
assert unreal.EditorAssetLibrary.save_loaded_asset(bp)
print(B.read_graph_dsl(graph))
settings = unreal.get_default_object(unreal.load_class(None, '/Script/UnrealEd.LevelEditorPlaySettings'))
unreal.ToolsetLibrary.set_object_properties(settings, '{"playNetMode":"PIE_Standalone"}')
for name, value in [('PlayNumberOfClients', 1), ('RunUnderOneProcess', True), ('NewWindowWidth',1280), ('NewWindowHeight',800)]:
    settings.set_editor_property(name,value)
print('DRAG_ANCHOR_FIXED_AND_COMPILED')
