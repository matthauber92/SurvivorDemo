from pathlib import Path
p=Path('MigrationStaging/test_inventory_mouse_drag.py');s=p.read_text().replace("src=ev('drag_coords(0)');dst=ev('drag_coords(6)');report['coordinates']={'source':src,'target':dst}",'''u.GetClientRect.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.RECT)]
 u.ClientToScreen.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.POINT)]
 rect=wintypes.RECT();u.GetClientRect(h,ctypes.byref(rect));origin=wintypes.POINT(0,0);u.ClientToScreen(h,ctypes.byref(origin))
 scale=rect.bottom/1080.0
 def pos(i):return (origin.x+rect.right*.5+(-418+(i%4)*211+98.5)*scale,origin.y+rect.bottom*.5+(-140+(i//4)*170+77.5)*scale)
 src=pos(0);dst=pos(6);report['coordinates']={'source':src,'target':dst}
 print('COORDS',report['coordinates'],flush=True)''')
s=s.replace("print(n,v);assert v,n","print(n,v,flush=True);assert v,n")
p.write_text(s)
