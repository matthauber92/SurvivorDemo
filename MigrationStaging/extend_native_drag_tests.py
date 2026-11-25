from pathlib import Path
p=Path('MigrationStaging/test_inventory_mouse_drag.py');s=p.read_text();needle=" report['passed']=True"
extra='''
 def drag_between(a,b,should_start=True):
  u.SetCursorPos(int(a[0]),int(a[1]));time.sleep(.15);u.mouse_event(2,0,0,0,0);time.sleep(.12)
  for step in range(1,11):
   u.SetCursorPos(int(a[0]+(b[0]-a[0])*step/10),int(a[1]+(b[1]-a[1])*step/10));time.sleep(.05)
  active=ev('unreal.WidgetLibrary.is_drag_dropping()')
  u.mouse_event(4,0,0,0,0);time.sleep(.8)
  return active
 check('occupied_slot_drag_starts',drag_between(pos(6),pos(1)))
 check('occupied_slots_swap',ev("[str(x.get_text()) for x in dui.get_editor_property('NameLabels')]")[1]=='First Aid Kit' and ev("[str(x.get_text()) for x in dui.get_editor_property('NameLabels')]")[6]=='Handgun Ammo')
 before=ev("list(di.get_editor_property('SlotOrder'))")
 check('cancel_drag_starts',drag_between(pos(1),(origin.x+rect.right*.04,origin.y+rect.bottom*.04)))
 check('outside_drop_keeps_items',ev("list(di.get_editor_property('SlotOrder'))")==before)
 check('cancel_restores_source_opacity',ev("dui.get_editor_property('SlotFrames')[1].get_render_opacity()")==1.0)
 check('empty_slot_does_not_drag',not drag_between(pos(0),pos(5),False))
 check('quantities_preserved',ev("list(di.get_editor_property('Quantities'))")==[3,10])
 check('server_matches_owner_layout',ev("list(next(p.get_controller() for w in unreal.EditorLevelLibrary.get_pie_worlds(False) for p in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Pawn) if p.has_authority() and not p.is_locally_controlled()).get_editor_property('InventoryComponent').get_editor_property('SlotOrder'))")==before)
 def key(k):u.keybd_event(k,0,0,0);time.sleep(.12);u.keybd_event(k,0,2,0);time.sleep(.5)
 key(0x49);check('I_closes_after_drag',not ev("dpc.get_editor_property('InventoryOpen')"))
 check('cursor_input_restored',ev("not dpc.get_editor_property('show_mouse_cursor') and not dpc.is_move_input_ignored() and not dpc.is_look_input_ignored()"))
 key(0x49);check('I_reopens_after_drag',ev("dpc.get_editor_property('InventoryOpen')"))
 code("dui=dpc.get_editor_property('InventoryWidget')")
 check('layout_preserved_on_reopen',ev("[str(x.get_text()) for x in dui.get_editor_property('NameLabels')]")[1]=='First Aid Kit')
 key(0x1B);check('Escape_closes_after_drag',not ev("dpc.get_editor_property('InventoryOpen')"))
'''
s=s.replace(needle,extra+needle);p.write_text(s)
