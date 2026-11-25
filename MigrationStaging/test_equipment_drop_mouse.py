import ctypes,time,sys,json,traceback
from ctypes import wintypes
from pathlib import Path
sys.path.insert(0,r'C:\Users\Matt Hauber\Epic Games\UE_5.8\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python')
import remote_execution
r=remote_execution.RemoteExecution();r.start();report={'checks':{},'method':'physical mouse drag in remote client PIE'}
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
pc=unreal.GameplayStatics.get_player_controller(cw,0);ui=pc.get_editor_property('InventoryWidget');inv=pc.get_editor_property('InventoryComponent')
ri=next(p.get_controller() for p in unreal.GameplayStatics.get_all_actors_of_class(sw,unreal.Pawn) if not p.is_locally_controlled()).get_editor_property('InventoryComponent')
def slots(i):return [i.call_method('GetInstanceAtLocation',(n,)) for n in range(11)]
def snapshot(i):return ([str(x) for x in i.get_editor_property('ItemIDs')],list(i.get_editor_property('Quantities')),slots(i),list(i.get_editor_property('WeaponMagazines')))
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
 rect=wintypes.RECT();u.GetClientRect(h,ctypes.byref(rect));origin=wintypes.POINT();u.ClientToScreen(h,ctypes.byref(origin));scale=rect.bottom/1080
 def pos(n):
  dx,dy=(-570+140,-190+(n-8)*135+62.5) if n>=8 else (-250+(n%4)*205+95,-180+(n//4)*180+82.5)
  return origin.x+rect.right*.5+dx*scale,origin.y+rect.bottom*.5+dy*scale
 def drag(source,target,stale=False):
  ax,ay=pos(source);bx,by=pos(target) if target>=0 else (origin.x+rect.right*.03,origin.y+rect.bottom*.04)
  u.SetCursorPos(int(ax),int(ay));time.sleep(.1);u.mouse_event(2,0,0,0,0);time.sleep(.12)
  for step in range(1,11):u.SetCursorPos(int(ax+(bx-ax)*step/10),int(ay+(by-ay)*step/10));time.sleep(.045)
  assert ev('unreal.WidgetLibrary.is_drag_dropping()'),'Drag did not start'
  if stale:run("ri.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_HandgunAmmo'),1))");time.sleep(.3)
  u.mouse_event(4,0,0,0,0);time.sleep(.7)
 ids=ev("list(inv.get_editor_property('WeaponInstances'))");p1,p2,l1,l2=ids
 def location(uid):return ev('slots(inv)').index(uid)
 before=ev('snapshot(inv)');drag(location(p1),8);check('incompatible_primary_rejected',ev('snapshot(inv)')==before)
 drag(location(p1),10);check('pistol_equipped_in_sidearm',ev('slots(inv)')[10]==p1);check('equipping_frees_backpack',ev("len(inv.get_editor_property('ItemIDs'))")==4)
 drag(location(p2),10);check('occupied_sidearm_atomic_swap',ev('slots(inv)')[10]==p2 and location(p1)<8)
 drag(location(l1),8);check('longgun_equipped_in_primary',ev('slots(inv)')[8]==l1)
 drag(location(l2),9);check('longgun_equipped_in_secondary',ev('slots(inv)')[9]==l2)
 ammo_slot=ev("next(n for n in range(8) if inv.get_editor_property('SlotOrder')[n]<len(inv.get_editor_property('ItemIDs')) and str(inv.get_editor_property('ItemIDs')[inv.get_editor_property('SlotOrder')[n]])=='Ammo.Handgun')")
 before=ev('snapshot(inv)');drag(ammo_slot,10);check('nonweapon_rejected_without_loss',ev('snapshot(inv)')==before)
 before=ev('snapshot(inv)');drag(location(p1),-1);check('outside_drop_cancels',ev('snapshot(inv)')==before)
 before=ev('slots(inv)');drag(location(p1),10,True);check('stale_drag_rejected',ev('slots(inv)')==before)
 target=next(n for n,s in enumerate(ev('slots(inv)')[:8]) if not s and n!=ammo_slot)
 drag(location(p1),target);check('backpack_reorder_preserved',location(p1)==target)
 check('client_matches_authority',ev('snapshot(inv)')==ev('snapshot(ri)'))
 check('all_weapon_instances_conserved',sorted(s for s in ev('slots(inv)') if s)==sorted(ids))
 check('host_inventory_unchanged',ev("len(unreal.GameplayStatics.get_player_controller(sw,0).get_editor_property('InventoryComponent').get_editor_property('ItemIDs'))")==0)
 check('drag_visual_cleaned_up',ev("ui.get_editor_property('CursorDragVisual') is None"))
 report['passed']=True
except Exception:report['error']=traceback.format_exc();report['passed']=False
finally:
 u.mouse_event(4,0,0,0,0);r.stop();Path('Saved/EquipmentValidation/equipment-drop-mouse-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
