from pathlib import Path
p=Path('MigrationStaging/build_inventory_ui_logic.py')
s=p.read_text().replace('Class|PlayerController|SetShowMouseCursor','Variables|MouseInterface|SetShowMouseCursor').replace('Class|PlayerController|GetShowMouseCursor','Variables|MouseInterface|GetShowMouseCursor').replace('str(p.pin_name)','str(unreal.BlueprintGraphPinLibrary.get_pin_name(p))')
s=s.replace('(== Key "(KeyName=I)")','(== Key (Variables|Default|GetToggleKey))').replace('(== Key "(KeyName=Escape)")','(== Key (Variables|Default|GetCloseKey))')
s=s.replace("# RepNotify notifies", "B.add_function_graph(inv,'NotifyInventoryChanged')\n# RepNotify notifies")
p.write_text(s)
