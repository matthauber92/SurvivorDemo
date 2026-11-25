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

 run("a=p.get_component_by_class(unreal.SkeletalMeshComponent).get_anim_instance();p.set_actor_location(unreal.Vector(-1500,-900,88),False,True);pc.set_control_rotation(unreal.Rotator())")
 def selected():return ev("a.get_editor_property('CurrentSelectedAnim').get_name()")
 def falling():return ev("p.get_component_by_class(unreal.CharacterMovementComponent).is_falling()")
 def snap(name):
  report.setdefault('samples',{})[name]={'animation':selected(),'falling':falling(),'speed':ev("a.get_editor_property('Speed2D')")}
 def jump_check(prefix):
  u.keybd_event(0x20,0x39,0,0);time.sleep(.08);u.keybd_event(0x20,0x39,2,0);time.sleep(.22)
  snap(prefix+'_air');check(prefix+'_airborne',falling());check(prefix+'_jump_animation','Jump' in selected() or 'Fall' in selected())
  run("unreal.SystemLibrary.execute_console_command(w,'Shot',pc)")
  time.sleep(1.5);snap(prefix+'_landed');check(prefix+'_landed',not falling());check(prefix+'_idle_after_landing','Idle' in selected())
 time.sleep(1.2);snap('unarmed_idle');check('unarmed_idle_animation','Idle' in selected())
 jump_check('unarmed_jump')
 u.keybd_event(0x57,0x11,0,0);time.sleep(1.1);snap('moving');check('moving_locomotion','Idle' not in selected() and not falling())
 u.keybd_event(0x57,0x11,2,0);time.sleep(1.6);snap('stopped');check('stop_returns_idle','Idle' in selected())
 run("inv.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_PistolItem'),1));uid=inv.get_editor_property('BackpackInstances')[0];inv.call_method('TryTransferWeapon',(0,10,uid,inv.get_editor_property('LayoutVersion')))")
 key(0x33,1.6);snap('armed_idle');check('armed_idle_locomotion','Idle' in selected());check('pistol_layer_active',ev("a.get_editor_property('PistolLayerWeight')")>.99)
 jump_check('armed_jump')
 u.mouse_event(8,0,0,0,0);time.sleep(.6);snap('aim_idle');check('aiming_keeps_idle','Idle' in selected());check('aim_crosshair_preserved',ev("p.get_editor_property('ShouldShowCrosshair')"));u.mouse_event(16,0,0,0,0)
 key(0x33,.6);check('holstering_removes_pistol_layer',ev("a.get_editor_property('PistolLayerWeight')")<.01)
 report['passed']=True
except Exception:report['error']=traceback.format_exc();report['passed']=False
finally:
 u.keybd_event(0x57,0x11,2,0);u.keybd_event(0x20,0x39,2,0);u.mouse_event(4,0,0,0,0);u.mouse_event(16,0,0,0,0);r.stop();Path('Saved/LocomotionRepair/controls-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
