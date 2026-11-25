import ctypes,time,sys,json,traceback
from ctypes import wintypes
from pathlib import Path
sys.path.insert(0,r'C:\Users\Matt Hauber\Epic Games\UE_5.8\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python')
import remote_execution
r=remote_execution.RemoteExecution();r.start();report={'checks':{},'method':'physical client mouse and keyboard'}
def run(s,mode=remote_execution.MODE_EXEC_FILE):
 q=r.run_command(s,exec_mode=mode)
 if not q['success']:raise RuntimeError(q)
 return q['result']
def ev(s):return eval(run(s,remote_execution.MODE_EVAL_STATEMENT),{'__builtins__':{}},{})
def check(n,b):report['checks'][n]=bool(b);assert b,n
u=ctypes.windll.user32;u.SetForegroundWindow.argtypes=[wintypes.HWND];u.GetForegroundWindow.restype=wintypes.HWND
u.GetWindowTextW.argtypes=[wintypes.HWND,wintypes.LPWSTR,ctypes.c_int];u.IsWindowVisible.argtypes=[wintypes.HWND]
try:
 for _ in range(30):
  if r.remote_nodes:break
  time.sleep(.2)
 r.open_command_connection(next(n for n in r.remote_nodes if n.get('project_name')=='AIExample')['node_id'])
 run("""import unreal
cw=next(w for w in unreal.EditorLevelLibrary.get_pie_worlds(False) if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
pc=unreal.GameplayStatics.get_player_controller(cw,0);ui=pc.get_editor_property('InventoryWidget');inv=pc.get_editor_property('InventoryComponent')
if not pc.get_editor_property('InventoryOpen'):pc.call_method('ToggleInventory');ui=pc.get_editor_property('InventoryWidget')
def equipment_coords(group,index):
 g=ui.get_editor_property(group)[index].get_cached_geometry()
 p=unreal.SlateLibrary.local_to_absolute(g,unreal.SlateLibrary.get_local_size(g)*0.5)
 return (p.x,p.y)
""")
 windows=[]
 @ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
 def cb(h,p):
  b=ctypes.create_unicode_buffer(512);u.GetWindowTextW(h,b,512)
  if u.IsWindowVisible(h) and 'AIExample Preview' in b.value and 'Client' in b.value:windows.append(h)
  return True
 u.EnumWindows(cb,0);h=windows[0]
 u.keybd_event(0x12,0,0,0);u.keybd_event(0x12,0,2,0);u.SetForegroundWindow(h);time.sleep(.3)
 check('client_focused',u.GetForegroundWindow()==h)
 u.GetClientRect.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.RECT)];u.ClientToScreen.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.POINT)]
 rect=wintypes.RECT();u.GetClientRect(h,ctypes.byref(rect));origin=wintypes.POINT(0,0);u.ClientToScreen(h,ctypes.byref(origin))
 scale=rect.bottom/1080.0
 def pos(group,i):
  dx,dy=(-570+140,-190+i*135+62.5) if group=='EquipmentFrames' else (-250+(i%4)*205+95,-180+(i//4)*180+82.5)
  return origin.x+rect.right*.5+dx*scale,origin.y+rect.bottom*.5+dy*scale
 def click(group,i,right=False):
  x,y=pos(group,i)
  u.SetCursorPos(int(x),int(y));time.sleep(.15)
  u.mouse_event(8 if right else 2,0,0,0,0);time.sleep(.1);u.mouse_event(16 if right else 4,0,0,0,0);time.sleep(.6)
 initial=ev("list(inv.get_editor_property('EquipmentInstances'))")
 click('EquipmentFrames',2,True)
 check('native_unequip_RPC',ev("list(inv.get_editor_property('EquipmentInstances'))")[2]=='')
 slot=ev("next(i for i in range(8) if inv.call_method('GetInstanceAtLocation',(i,))=="+repr(initial[2])+")")
 click('SlotFrames',slot);click('EquipmentFrames',2)
 check('native_equip_RPC',ev("list(inv.get_editor_property('EquipmentInstances'))")==initial)
 source=ev("next(i for i in range(8) if inv.call_method('GetInstanceAtLocation',(i,)))")
 target=ev("next(i for i in range(8) if not inv.call_method('GetInstanceAtLocation',(i,)))")
 uid=ev("inv.call_method('GetInstanceAtLocation',("+str(source)+",))")
 ax,ay=pos('SlotFrames',source);bx,by=pos('SlotFrames',target)
 u.SetCursorPos(int(ax),int(ay));time.sleep(.2);u.mouse_event(2,0,0,0,0);time.sleep(.15)
 for step in range(1,11):u.SetCursorPos(int(ax+(bx-ax)*step/10),int(ay+(by-ay)*step/10));time.sleep(.06)
 check('backpack_drag_starts',ev('unreal.WidgetLibrary.is_drag_dropping()'))
 u.mouse_event(4,0,0,0,0);time.sleep(.8)
 check('backpack_drag_preserves_instance',ev("inv.call_method('GetInstanceAtLocation',("+str(target)+",))")==uid)
 def key(k):u.keybd_event(k,0,0,0);time.sleep(.12);u.keybd_event(k,0,2,0);time.sleep(.6)
 key(0x49);check('I_closes',not ev("pc.get_editor_property('InventoryOpen')"))
 report['foreground_after_close_is_client']=u.GetForegroundWindow()==h
 key(0x49);check('I_reopens',ev("pc.get_editor_property('InventoryOpen')"))
 report['passed']=True
except Exception:report['error']=traceback.format_exc();report['passed']=False
finally:
 u.mouse_event(4,0,0,0,0);u.mouse_event(16,0,0,0,0);r.stop()
 Path('Saved/EquipmentValidation/mouse-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
