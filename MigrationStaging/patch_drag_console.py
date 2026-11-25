from pathlib import Path
p=Path('MigrationStaging/build_inventory_drag_server.py');s=p.read_text().replace("d.set_editor_property('command_name','set '+e.get_path_name()+' '+prop);d.set_editor_property('command_value',value)","d.import_text('(CommandName=\"set '+e.get_path_name()+' '+prop+'\",CommandValueAsString=\"'+value+'\",CheckedState=Checked)')")
p.write_text(s)
