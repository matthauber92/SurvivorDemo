import ctypes,time,sys,json,traceback
from ctypes import wintypes
from pathlib import Path
sys.path.insert(0,r'C:\Users\Matt Hauber\Epic Games\UE_5.8\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python')
import remote_execution
r=remote_execution.RemoteExecution();r.start();report={'checks':{},'method':'physical keyboard input in remote client PIE'}
def run(s,mode=remote_execution.MODE_EXEC_FILE):
 q=r.run_command(s,exec_mode=mode)
 if not q['success']:raise RuntimeError(q)
 return q['result']
def ev(s):return eval(run(s,remote_execution.MODE_EVAL_STATEMENT),{'__builtins__':{}},{})
def check(n,b):report['checks'][n]=bool(b);print(n,b,flush=True);assert b,n
u=ctypes.windll.user32;u.SetForegroundWindow.argtypes=[wintypes.HWND];u.GetForegroundWindow.restype=wintypes.HWND
u.GetWindowTextW.argtypes=[wintypes.HWND,wintypes.LPWSTR,ctypes.c_int];u.IsWindowVisible.argtypes=[wintypes.HWND]
try:
 for _ in range(30):
  if r.remote_nodes:break
  time.sleep(.2)
 r.open_command_connection(next(n for n in r.remote_nodes if n.get('project_name')=='AIExample')['node_id'])
 run('''import unreal
cw=next(w for w in unreal.EditorLevelLibrary.get_pie_worlds(False) if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
sw=next(w for w in unreal.EditorLevelLibrary.get_pie_worlds(False) if unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
cpc=unreal.GameplayStatics.get_player_controller(cw,0);cp=cpc.get_controlled_pawn()
rp=next(p for p in unreal.GameplayStatics.get_all_actors_of_class(sw,unreal.Pawn) if not p.is_locally_controlled())
''')
 windows=[]
 @ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
 def cb(h,p):
  b=ctypes.create_unicode_buffer(512);u.GetWindowTextW(h,b,512)
  if u.IsWindowVisible(h) and 'AIExample Preview' in b.value and 'Client' in b.value:windows.append(h)
  return True
 u.EnumWindows(cb,0);h=windows[0];u.keybd_event(18,0,0,0);u.keybd_event(18,0,2,0);u.SetForegroundWindow(h);time.sleep(.4)
 check('client_focused',u.GetForegroundWindow()==h)
 u.GetClientRect.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.RECT)];u.ClientToScreen.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.POINT)]
 rect=wintypes.RECT();u.GetClientRect(h,ctypes.byref(rect));origin=wintypes.POINT();u.ClientToScreen(h,ctypes.byref(origin))
 u.SetCursorPos(origin.x+rect.right//2,origin.y+rect.bottom//2);u.mouse_event(2,0,0,0,0);u.mouse_event(4,0,0,0,0);time.sleep(.2)
 def key(k,hold=.1):u.keybd_event(k,0,0,0);time.sleep(hold);u.keybd_event(k,0,2,0);time.sleep(.6)
 def slots():return ev("(cp.get_editor_property('PublicActiveSlot'),rp.get_editor_property('PublicActiveSlot'))")
 key(0x33);check('three_draws_pistol',slots()==(2,2))
 key(0x31);check('one_switches_primary',slots()==(0,0))
 key(0x32);check('two_switches_secondary',slots()==(1,1))
 key(0x32,1.0);check('held_key_only_toggles_once',slots()==(-1,-1))
 key(0x49);check('inventory_opens',ev("cpc.get_editor_property('InventoryOpen')"))
 key(0x33);check('inventory_blocks_number_keys',slots()==(-1,-1))
 key(0x49);check('inventory_closes',not ev("cpc.get_editor_property('InventoryOpen')"))
 key(0x33);check('pistol_draws_after_inventory',slots()==(2,2))
 report['passed']=True
except Exception:report['error']=traceback.format_exc();report['passed']=False
finally:
 r.stop();Path('Saved/WeaponSwitchValidation/keyboard-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
