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
 key(0x33,1.6);check('three_draws_pistol',ev("p.get_editor_property('PublicActiveSlot')")==2)
 fire();check('empty_click_does_not_fire',ev('mag()')==0 and ev("p.get_editor_property('PublicShotSerial')")==0 and ev("inv.get_editor_property('DryFireSerial')")>0)
 key(0x52,.3);check('R_starts_reload',ev("inv.get_editor_property('Reloading')"));time.sleep(2.1)
 check('reload_moves_15_rounds',ev('(mag(),reserve())')==(15,15))
 u.mouse_event(8,0,0,0,0);time.sleep(.5);check('RMB_aims',ev("p.get_editor_property('PublicAiming')"))
 for _ in range(10):
  run('pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(unreal.GameplayStatics.get_player_camera_manager(w,0).get_camera_location(),target.get_actor_location()))');time.sleep(.12)
 fire();check('shot_spends_one_round',ev('mag()')==14);check('shot_damages_target',ev("target.get_editor_property('Health')")==75)
 check('shot_effect_event_fired',ev("p.get_editor_property('PublicShotSerial')")==1)
 u.mouse_event(2,0,0,0,0);time.sleep(.7);u.mouse_event(4,0,0,0,0);time.sleep(.3);check('semi_auto_fires_once_per_press',ev('mag()')==13)
 u.mouse_event(16,0,0,0,0);time.sleep(.3);check('release_RMB_stops_aim',not ev("p.get_editor_property('PublicAiming')"))
 key(0x52,.2);check('partial_reload_starts',ev("inv.get_editor_property('Reloading')"));key(0x33,.4)
 check('holster_cancels_reload_without_ammo_loss',not ev("inv.get_editor_property('Reloading')") and ev('(mag(),reserve())')==(13,15))
 key(0x33,1.6);key(0x52,2.3);check('partial_reload_only_tops_up',ev('(mag(),reserve())')==(15,13))
 key(0x49,.3);before=ev('mag()');fire();check('inventory_blocks_fire',ev('mag()')==before);key(0x49,.3)
 report['passed']=True
except Exception:report['error']=traceback.format_exc();report['passed']=False
finally:
 u.mouse_event(4,0,0,0,0);u.mouse_event(16,0,0,0,0);r.stop();Path('Saved/PistolCombatValidation/keyboard-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
