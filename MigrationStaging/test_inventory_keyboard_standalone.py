"""Physical keyboard regression test against the running standalone preview."""
import ctypes,time,sys,json,traceback
from ctypes import wintypes
from pathlib import Path
sys.path.insert(0,r'C:\Users\Matt Hauber\Epic Games\UE_5.8\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python')
import remote_execution
r=remote_execution.RemoteExecution();r.start();report={'mode':'PIE standalone net mode','method':'physical Windows keys, runtime state assertions','checks':{}}
def check(n,v):report['checks'][n]=bool(v);print(n,bool(v));assert v,n
def code(s):
 result=r.run_command(s)
 if not result['success']:raise RuntimeError(result)
 return result
def evaluate(s):
 result=r.run_command(s,exec_mode=remote_execution.MODE_EVAL_STATEMENT)
 if not result['success']:raise RuntimeError(result)
 return eval(result['result'],{'__builtins__':{}},{})
u=ctypes.windll.user32;u.IsWindowVisible.argtypes=[wintypes.HWND];u.GetWindowTextW.argtypes=[wintypes.HWND,wintypes.LPWSTR,ctypes.c_int];u.SetForegroundWindow.argtypes=[wintypes.HWND];u.GetWindowRect.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.RECT)]
def press(key,click=False):
 windows=[]
 @ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
 def cb(h,p):
  b=ctypes.create_unicode_buffer(512);u.GetWindowTextW(h,b,512)
  if u.IsWindowVisible(h) and 'AIExample Preview' in b.value:windows.append(h)
  return True
 u.EnumWindows(cb,0);assert len(windows)==1
 h=windows[0];u.keybd_event(0x12,0,0,0);u.keybd_event(0x12,0,2,0);u.SetForegroundWindow(h);time.sleep(.2)
 if click:
  rect=wintypes.RECT();u.GetWindowRect(h,ctypes.byref(rect));u.SetCursorPos((rect.left+rect.right)//2,(rect.top+rect.bottom)//2);u.mouse_event(2,0,0,0,0);time.sleep(.1);u.mouse_event(4,0,0,0,0);time.sleep(.2)
 u.keybd_event(key,0,0,0);time.sleep(.12);u.keybd_event(key,0,2,0);time.sleep(.6)
try:
 for _ in range(20):
  if r.remote_nodes:break
  time.sleep(.2)
 r.open_command_connection(next(n for n in r.remote_nodes if n.get('project_name')=='AIExample')['node_id'])
 code("""import unreal
w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0]
pc=unreal.GameplayStatics.get_player_controller(w,0);pawn=unreal.GameplayStatics.get_player_pawn(w,0);inv=pc.get_editor_property('InventoryComponent')
pc.call_method('CloseInventory')
pawn.set_actor_location(unreal.Vector(-180,0,90),False,True);pc.set_control_rotation(unreal.Rotator())
""")
 time.sleep(.7);press(0x45,True)
 check('E_pickup',evaluate("list(inv.get_editor_property('Quantities'))")==[30])
 press(0x49)
 check('I_opens',evaluate("pc.get_editor_property('InventoryOpen')"))
 code("widget=pc.get_editor_property('InventoryWidget')")
 check('eight_slots',evaluate("len(widget.get_editor_property('NameLabels'))")==8)
 check('collected_name_quantity',evaluate("(str(widget.get_editor_property('NameLabels')[0].get_text()),str(widget.get_editor_property('QuantityLabels')[0].get_text()))")==('Handgun Ammo','30'))
 check('seven_empty_slots',evaluate("[str(x.get_text()) for x in widget.get_editor_property('NameLabels')][1:]")==['EMPTY']*7)
 check('occupied_count',evaluate("str(widget.get_editor_property('OccupiedLabel').get_text())")=='1 / 8 SLOTS OCCUPIED')
 check('cursor_and_input_gates',evaluate("pc.get_editor_property('show_mouse_cursor') and pc.is_move_input_ignored() and pc.is_look_input_ignored()"))
 check('not_paused',not evaluate("unreal.GameplayStatics.is_game_paused(w)"))
 before=evaluate('unreal.GameplayStatics.get_time_seconds(w)');time.sleep(.7)
 check('world_keeps_ticking',evaluate('unreal.GameplayStatics.get_time_seconds(w)')>before+.2)
 code("inv.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_HandgunAmmo'),45))")
 check('open_UI_refreshes_server_changes',evaluate("[str(x.get_text()) for x in widget.get_editor_property('QuantityLabels')][:2]")==['60','15'])
 press(0x49)
 check('I_closes',not evaluate("pc.get_editor_property('InventoryOpen')"))
 check('cursor_and_input_restored',evaluate("not pc.get_editor_property('show_mouse_cursor') and not pc.is_move_input_ignored() and not pc.is_look_input_ignored()"))
 press(0x49);check('I_reopens',evaluate("pc.get_editor_property('InventoryOpen')"))
 press(0x1B);check('Escape_closes_without_ending_PIE',evaluate("len(unreal.EditorLevelLibrary.get_pie_worlds(False))==1 and not pc.get_editor_property('InventoryOpen')"))
 code("pawn.set_actor_location(unreal.Vector(620,0,90),False,True);pc.set_control_rotation(unreal.Rotator())")
 time.sleep(.7);press(0x45)
 check('E_door_after_closing',evaluate("all(a.get_editor_property('IsOpen') for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/AIExample/Interaction/BP_InteractionTestDoor.BP_InteractionTestDoor_C')))"))
 code("pc.call_method('ToggleInventory');inv.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_Key'),6));widget=pc.get_editor_property('InventoryWidget')")
 check('full_eight_slots',evaluate("str(widget.get_editor_property('OccupiedLabel').get_text())")=='8 / 8 SLOTS OCCUPIED')
 code("pc.call_method('CloseInventory')")
 report['passed']=all(report['checks'].values())
except Exception:report['error']=traceback.format_exc();report['passed']=False;print(report['error'])
finally:
 r.stop();Path('Saved/InventoryUIValidation/standalone-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

