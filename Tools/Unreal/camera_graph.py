import unreal
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from toolset_registry import tool_raising_exceptions


def pin_snapshot(nodes):
    snapshot = {}
    for node in nodes:
        for index, pin in enumerate(node.list_all_pins()):
            links = tuple((link.get_owning_node().get_name(), str(link.get_pin_name()))
                          for link in pin.list_connected_pins() if link.get_owning_node() in nodes)
            snapshot[node.get_name(), index] = (str(pin.get_pin_name()), str(pin.get_pin_type_display_string()),
                                                str(pin.get_pin_direction()), str(pin.get_pin_value()), links)
    return snapshot


def prune_camera_graph(graph, expected_counts=None):
    """Keep execution reachable from entry and the data feeding that execution."""
    assert graph.get_name() == 'FrameAnkleBite'
    nodes = set(B.find_nodes(graph))
    entry, = [node for node in nodes if isinstance(node, unreal.K2Node_FunctionEntry)]
    output = unreal.EdGraphPinDirection.EGPD_OUTPUT
    inputs = unreal.EdGraphPinDirection.EGPD_INPUT

    def closure(seeds, direction, exec_pins):
        visited = set(seeds)
        pending = list(visited)
        while pending:
            for pin in pending.pop().list_all_pins():
                if pin.get_pin_direction() != direction:
                    continue
                if (str(pin.get_pin_type_display_string()).lower() == 'exec') != exec_pins:
                    continue
                for link in pin.list_connected_pins():
                    node = link.get_owning_node()
                    if node not in visited:
                        visited.add(node)
                        pending.append(node)
        return visited

    executed = closure([entry], output, True)
    assert len(executed) > 1
    protected = {node for node in nodes if node.get_class().get_name() in
                 {'EdGraphNode_Comment', 'K2Node_FunctionResult'}}
    active = closure(executed | protected, inputs, False)
    stale = nodes - active
    if expected_counts is not None:
        assert (len(nodes), len(active)) == expected_counts
    disposable = {'K2Node_PromotableOperator', 'K2Node_CallFunction', 'K2Node_VariableSet',
                  'K2Node_VariableGet', 'K2Node_IfThenElse', 'K2Node_CommutativeAssociativeBinaryOperator'}
    assert all(node.get_class().get_name() in disposable for node in stale)
    if stale:
        with tool_raising_exceptions():
            before = pin_snapshot(active)
            unreal.BlueprintGraphEditor.get_graph_editor(graph).remove_nodes(list(stale))
            assert set(B.find_nodes(graph)) == active
            assert pin_snapshot(active) == before, 'Camera graph changed during pruning'
    return len(stale), len(active)


