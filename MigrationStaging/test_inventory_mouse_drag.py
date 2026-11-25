import ctypes,time,sys,json,traceback
from ctypes import wintypes
from pathlib import Path
sys.path.insert(0,r'C:\Users\Matt Hauber\Epic Games\UE_5.8\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python')
import remote_execution
r=remote_execution.RemoteExecution();r.start();report={'method':'physical mouse drag in client PIE window','checks':{}}
def code(s):
 q=r.run_command(s)
 if not q['success']:raise RuntimeError(q)
def ev(s):
 q=r.run_command(s,exec_mode=remote_execution.MODE_EVAL_STATEMENT)
 if not q['success']:raise RuntimeError(q)
 return eval(q['result'],{'__builtins__':{}},{})
def check(n,v):report['checks'][n]=bool(v);print(n,v,flush=True);assert v,n
u=ctypes.windll.user32;u.IsWindowVisible.argtypes=[wintypes.HWND];u.GetWindowTextW.argtypes=[wintypes.HWND,wintypes.LPWSTR,ctypes.c_int];u.SetForegroundWindow.argtypes=[wintypes.HWND];u.GetForegroundWindow.restype=wintypes.HWND
try:
 for _ in range(30):
  if r.remote_nodes:break
  time.sleep(.2)
 r.open_command_connection(next(n for n in r.remote_nodes if n.get('project_name')=='AIExample')['node_id'])
 code("""import unreal
cw=next(w for w in unreal.EditorLevelLibrary.get_pie_worlds(False) if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
dpc=unreal.GameplayStatics.get_player_controller(cw,0);dui=dpc.get_editor_property('InventoryWidget');di=dpc.get_editor_property('InventoryComponent')
def drag_coords(slot):
 geometry=dui.get_editor_property('SlotFrames')[slot].get_cached_geometry()
 v=unreal.SlateLibrary.local_to_absolute(geometry,unreal.SlateLibrary.get_local_size(geometry)*0.5)
 return (v.x,v.y)
""")
 windows=[]
 @ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
 def cb(h,p):
  b=ctypes.create_unicode_buffer(512);u.GetWindowTextW(h,b,512)
  if u.IsWindowVisible(h) and 'AIExample Preview' in b.value:windows.append((h,b.value))
  return True
 u.EnumWindows(cb,0);print(windows)
 h=next(h for h,title in windows if 'Client' in title)
 u.keybd_event(0x12,0,0,0);u.keybd_event(0x12,0,2,0);u.SetForegroundWindow(h);time.sleep(.3)
 check('client_window_focused',u.GetForegroundWindow()==h)
 u.GetClientRect.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.RECT)]
 u.ClientToScreen.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.POINT)]
 rect=wintypes.RECT();u.GetClientRect(h,ctypes.byref(rect));origin=wintypes.POINT(0,0);u.ClientToScreen(h,ctypes.byref(origin))
 scale=rect.bottom/1080.0
 def pos(i):return (origin.x+rect.right*.5+(-418+(i%4)*211+98.5)*scale,origin.y+rect.bottom*.5+(-140+(i//4)*170+77.5)*scale)
 src=pos(0);dst=pos(6);report['coordinates']={'source':src,'target':dst}
 print('COORDS',report['coordinates'],flush=True)
 u.SetCursorPos(int(src[0]),int(src[1]));time.sleep(.2);u.mouse_event(2,0,0,0,0);time.sleep(.15)
 for step in range(1,11):
  u.SetCursorPos(int(src[0]+(dst[0]-src[0])*step/10),int(src[1]+(dst[1]-src[1])*step/10));time.sleep(.07)
 check('native_drag_operation_started',ev('unreal.WidgetLibrary.is_drag_dropping()'))
 code("unreal.SystemLibrary.execute_console_command(cw,'Shot showui',dpc)")
 u.mouse_event(4,0,0,0,0);time.sleep(1)
 check('mouse_drop_replicates',ev("list(di.get_editor_property('SlotOrder'))")==[6,1,2,3,4,5,0,7])
 check('UI_moved_to_empty_slot',ev("str(dui.get_editor_property('NameLabels')[6].get_text())")=='First Aid Kit')

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
 report['passed']=True
except Exception:report['error']=traceback.format_exc();report['passed']=False;print(report['error'])
finally:
 u.mouse_event(4,0,0,0,0);r.stop();Path('Saved/InventoryDragValidation/mouse-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
