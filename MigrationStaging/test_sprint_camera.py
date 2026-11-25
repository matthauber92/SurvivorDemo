import ctypes,time,sys,json,traceback
from ctypes import wintypes
from pathlib import Path
sys.path.insert(0,r'C:\Users\Matt Hauber\Epic Games\UE_5.8\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python')
import remote_execution
r=remote_execution.RemoteExecution();r.start();report={'checks':{},'method':'physical mouse and keyboard in standalone PIE'}
def run(s,mode=remote_execution.MODE_EXEC_FILE):
 q=r.run_command(s,exec_mode=mode)
 if not q['success']:raise RuntimeError(q)
 return q['result']
def ev(s):return eval(run(s,remote_execution.MODE_EVAL_STATEMENT),{'__builtins__':{}},{})
def check(n,b):report['checks'][n]=bool(b);print(n,b,flush=True);assert b,n
u=ctypes.windll.user32;u.SetForegroundWindow.argtypes=[wintypes.HWND];u.GetForegroundWindow.restype=wintypes.HWND;u.GetWindowTextW.argtypes=[wintypes.HWND,wintypes.LPWSTR,ctypes.c_int];u.IsWindowVisible.argtypes=[wintypes.HWND]
try:
 for _ in range(30):
  if r.remote_nodes:break
  time.sleep(.2)
 r.open_command_connection(next(n for n in r.remote_nodes if n.get('project_name')=='AIExample')['node_id'])
 run('''import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0];p=unreal.GameplayStatics.get_player_pawn(w,0);pc=p.get_controller();inv=pc.get_editor_property('InventoryComponent')
target=min(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Combat/BP_PistolTarget.BP_PistolTarget_C')),key=lambda a:(a.get_actor_location()-p.get_actor_location()).length())
def mag():return inv.get_editor_property('WeaponMagazines')[0]
def reserve():return inv.call_method('GetItemQuantity',(unreal.Name('Ammo.Handgun'),))
''')
 windows=[]
 @ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
 def cb(h,p):
  b=ctypes.create_unicode_buffer(512);u.GetWindowTextW(h,b,512)
  if u.IsWindowVisible(h) and 'AIExample Preview' in b.value:windows.append(h)
  return True
 u.EnumWindows(cb,0);h=windows[0];u.keybd_event(18,0,0,0);u.keybd_event(18,0,2,0);u.SetForegroundWindow(h);time.sleep(.3)
 check('preview_focused',u.GetForegroundWindow()==h)
 u.GetClientRect.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.RECT)];u.ClientToScreen.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.POINT)]
 rect=wintypes.RECT();u.GetClientRect(h,ctypes.byref(rect));pt=wintypes.POINT();u.ClientToScreen(h,ctypes.byref(pt));u.SetCursorPos(pt.x+rect.right//2,pt.y+rect.bottom//2);u.mouse_event(2,0,0,0,0);u.mouse_event(4,0,0,0,0)
 def key(k,wait=.35):u.keybd_event(k,0,0,0);time.sleep(.06);u.keybd_event(k,0,2,0);time.sleep(wait)
 def fire(wait=.3):u.mouse_event(2,0,0,0,0);time.sleep(.06);u.mouse_event(4,0,0,0,0);time.sleep(wait)

 run("p.set_actor_location(unreal.Vector(-1200,0,88),False,True);pc.set_control_rotation(unreal.Rotator())")
 u.keybd_event(0x57,0x11,0,0);time.sleep(.5);u.keybd_event(0xA0,0x2A,0,0);time.sleep(1.7)
 print(run("print('STATE',p.get_editor_property('CharacterInputState'),p.get_velocity(),p.get_editor_property('ShoulderBoom').get_editor_property('target_arm_length'),p.get_actor_location())"),flush=True)
 print('ARM',ev("p.get_editor_property('ShoulderBoom').get_editor_property('target_arm_length')"),flush=True)
 check('sprint_camera_pulls_back',ev("p.get_editor_property('ShoulderBoom').get_editor_property('target_arm_length')")>590)
 check('sprint_crosshair_hidden',not ev("p.get_editor_property('ShouldShowCrosshair')"))
 run("unreal.SystemLibrary.execute_console_command(w,'Shot',pc)")
 u.keybd_event(0x57,0x11,2,0);u.keybd_event(0xA0,0x2A,2,0);time.sleep(1.5)
 check('stopping_restores_close_camera',abs(ev("p.get_editor_property('ShoulderBoom').get_editor_property('target_arm_length')")-350)<2)
 report['passed']=True
except Exception:report['error']=traceback.format_exc();report['passed']=False
finally:
 u.keybd_event(0x57,0,2,0);u.keybd_event(0xA0,0x2A,2,0);u.mouse_event(4,0,0,0,0);u.mouse_event(16,0,0,0,0);r.stop();Path('Saved/ShoulderCamera/sprint-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
