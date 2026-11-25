from pathlib import Path
p=Path('MigrationStaging/inventory_keyboard.py');s=p.read_text()
s=s.replace('h=windows[idx][0];u.SetForegroundWindow(h);time.sleep(.3)', '''h=windows[idx][0]
 u.GetForegroundWindow.restype=wintypes.HWND
 u.GetWindowRect.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.RECT)]
 u.keybd_event(0x12,0,0,0);u.keybd_event(0x12,0,2,0)
 focused=u.SetForegroundWindow(h);time.sleep(.3)
 print('FOREGROUND',focused,u.GetForegroundWindow(),h)
 if len(sys.argv)>3 and sys.argv[3]=='click':
  rect=wintypes.RECT();u.GetWindowRect(h,ctypes.byref(rect));u.SetCursorPos((rect.left+rect.right)//2,(rect.top+rect.bottom)//2)
  u.mouse_event(2,0,0,0,0);time.sleep(.1);u.mouse_event(4,0,0,0,0);time.sleep(.3)''')
p.write_text(s)
