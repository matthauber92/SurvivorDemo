from pathlib import Path
p=Path('MigrationStaging/build_inventory_drag_ui.py');s=p.read_text().replace('(return (Widget|DragandDrop|EventReply|DetectDragifPressed :PointerEvent MouseEvent :DragKey (Variables|Default|GetDragKey)))','(bind Reply (Widget|DragandDrop|EventReply|DetectDragifPressed :PointerEvent MouseEvent :DragKey (Variables|Default|GetDragKey))) (return Reply)');p.write_text(s)
