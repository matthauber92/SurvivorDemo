from pathlib import Path
s=Path('MigrationStaging/test_inventory_mouse_drag.py').read_text().replace("'method':'physical mouse drag in client PIE window'","'method':'physical mouse drag in standalone PIE'")
s=s.replace("cw=next(w for w in unreal.EditorLevelLibrary.get_pie_worlds(False) if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())", "cw=unreal.EditorLevelLibrary.get_pie_worlds(False)[0]")
s=s.replace("dpc=unreal.GameplayStatics.get_player_controller(cw,0);dui=dpc.get_editor_property('InventoryWidget');di=dpc.get_editor_property('InventoryComponent')", "dpc=unreal.GameplayStatics.get_player_controller(cw,0);di=dpc.get_editor_property('InventoryComponent')\ndi.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_FirstAidKit'),3));di.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_HandgunAmmo'),10));dpc.call_method('ToggleInventory');dui=dpc.get_editor_property('InventoryWidget')")
s=s.replace("if 'Client' in title", "if 'Standalone' in title")
s='\n'.join(line for line in s.splitlines() if "check('server_matches_owner_layout'" not in line)
s=s.replace('mouse-result.json','standalone-mouse-result.json')
Path('MigrationStaging/test_inventory_mouse_drag_standalone.py').write_text(s)
