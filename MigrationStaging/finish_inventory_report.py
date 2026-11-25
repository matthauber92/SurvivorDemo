import json
from pathlib import Path
out=Path('Saved/InventoryUIValidation');p=out/'milestone4-report.json';report=json.loads(p.read_text())
report['status']='Implemented; PIE checks passed; separate-process physical keyboard verification remains manual.'
report['validation']['separate_process_standalone']={'runtime_probe':json.loads((out/'standalone-probe.json').read_text()),'physical_keyboard':'Inconclusive. Automated captures did not show the inventory; physical I/Escape must be verified manually in Standalone Game. Startup timing and desktop focus affected the harness; this is not counted as a pass.','launch_notes':'The existing editor toolset Python startup reports missing AgentSkill/PythonTestRunner in -game mode. Gameplay starts, and the runtime probe confirmed the expected controller, character, mapping context, and widget creation.'}
report['manual_checks_remaining'].insert(0,'Separate-process Standalone Game: manually verify I opens/closes and Escape closes, then movement/mouse capture restoration. PIE standalone mode passed the physical-key test; separate-process keyboard automation is inconclusive.')
report['validation']['final_input_binding_check']=json.loads((out/'final-input-binding-check.json').read_text())
report['validation']['passed_PIE_UI_checks']=sum(len(report['validation'][n]['checks']) for n in ['standalone','multiplayer'])
p.write_text(json.dumps(report,indent=2))
# Keep the builder consistent with the final asset: discard unconnected input-event prototypes.
p=Path('MigrationStaging/build_inventory_ui_logic.py');s=p.read_text();marker="B.add_function_graph(inv,'NotifyInventoryChanged')"
cleanup="""for unused in list(B.find_nodes(g)):
 if isinstance(unused,unreal.K2Node_EnhancedInputAction) and not any(p.connected_pins for p in B._get_node_info(unused).output_pins):B.delete_node(unused)
"""
if cleanup not in s:s=s.replace(marker,cleanup+marker)
p.write_text(s)
print('REPORT_FINALIZED',report['validation']['passed_PIE_UI_checks'])
