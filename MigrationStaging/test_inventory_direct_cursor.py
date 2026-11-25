import ctypes,time,sys,json,traceback
from ctypes import wintypes
from pathlib import Path
sys.path.insert(0,r'C:\Users\Matt Hauber\Epic Games\UE_5.8\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python')
import remote_execution
r=remote_execution.RemoteExecution();r.start();report={'method':'physical mouse drag in standalone PIE','checks':{}}
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
cw=unreal.EditorLevelLibrary.get_pie_worlds(False)[0]
dpc=unreal.GameplayStatics.get_player_controller(cw,0);di=dpc.get_editor_property('InventoryComponent')
di.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_FirstAidKit'),3));di.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_HandgunAmmo'),10));dpc.call_method('ToggleInventory');dui=dpc.get_editor_property('InventoryWidget')
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
 h=next(h for h,title in windows if 'Standalone' in title)
 u.keybd_event(0x12,0,0,0);u.keybd_event(0x12,0,2,0);u.SetForegroundWindow(h);time.sleep(.3)
 check('client_window_focused',u.GetForegroundWindow()==h)
 u.GetClientRect.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.RECT)]
 u.ClientToScreen.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.POINT)]
 rect=wintypes.RECT();u.GetClientRect(h,ctypes.byref(rect));origin=wintypes.POINT(0,0);u.ClientToScreen(h,ctypes.byref(origin))
 scale=rect.bottom/1080.0
 def pos(i):return (origin.x+rect.right*.5+(-418+(i%4)*211+98.5)*scale,origin.y+rect.bottom*.5+(-140+(i//4)*170+77.5)*scale)
 src=pos(0)
 u.SetCursorPos(int(src[0]),int(src[1]));time.sleep(.1);u.mouse_event(2,0,0,0,0);time.sleep(.12)
 u.SetCursorPos(int(src[0]+20),int(src[1]+10));time.sleep(.025)
 check('drag_started',ev('unreal.WidgetLibrary.is_drag_dropping()'))
 code("cv=dui.get_editor_property('CursorDragVisual');dop=unreal.WidgetLibrary.get_drag_dropping_content();vp=unreal.get_engine_subsystem(unreal.GameViewportSubsystem)")
 check('visible_widget_bypasses_animated_decorator',ev("cv.is_in_viewport() and cv != dop.get_editor_property('default_drag_visual')"))
 check('animated_proxy_empty',ev("unreal.find_object(unreal.find_object(unreal.load_asset('/Game/AIExample/UI/WBP_InventoryDragProxy'),'WidgetTree'),'Overlay_19').get_children_count()==0"))
 def aligned(x,y):
  code("cs=vp.get_widget_slot(cv)")
  xy=ev("(cs.offsets.left,cs.offsets.top,cs.alignment.x,cs.alignment.y)")
  code("mp=unreal.WidgetLayoutLibrary.get_mouse_position_on_viewport(cw)")
  expected=ev('(mp.x,mp.y)')
  print('POSITION',xy,'EXPECTED',expected,flush=True)
  return abs(xy[0]-expected[0])<2 and abs(xy[1]-expected[1])<2 and xy[2:]==(.5,.5)
 check('initial_cursor_position_exact',aligned(src[0]+20,src[1]+10))
 dst=pos(7);u.SetCursorPos(int(dst[0]),int(dst[1]));time.sleep(.025)
 check('cursor_position_updates_without_lerp',aligned(*dst))
 u.mouse_event(4,0,0,0,0);time.sleep(.3)
 check('drop_removes_visual',ev("not cv.is_in_viewport() and dui.get_editor_property('CursorDragVisual') is None"))
 u.SetCursorPos(int(dst[0]),int(dst[1]));u.mouse_event(2,0,0,0,0);time.sleep(.12);u.SetCursorPos(int(dst[0]+20),int(dst[1]+10));time.sleep(.1)
 code("cv=dui.get_editor_property('CursorDragVisual')")
 check('second_drag_started',ev('unreal.WidgetLibrary.is_drag_dropping()'))
 code("dpc.call_method('CloseInventory')")
 check('closing_during_drag_removes_visual',ev("not cv.is_in_viewport() and not unreal.WidgetLibrary.is_drag_dropping() and not dpc.get_editor_property('InventoryOpen')"))
 report['passed']=True
except Exception:
 report['error']=traceback.format_exc();report['passed']=False;print(report['error'])
finally:
 u.mouse_event(4,0,0,0,0);r.stop();Path('Saved/InventoryDragValidation/direct-cursor-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))


