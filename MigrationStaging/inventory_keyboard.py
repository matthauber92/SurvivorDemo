import ctypes,time,sys
from ctypes import wintypes
u=ctypes.windll.user32
u.IsWindowVisible.argtypes=[wintypes.HWND]
u.GetWindowTextW.argtypes=[wintypes.HWND,wintypes.LPWSTR,ctypes.c_int]
u.SetForegroundWindow.argtypes=[wintypes.HWND]
windows=[]
@ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
def cb(h,p):
 if u.IsWindowVisible(h):
  buf=ctypes.create_unicode_buffer(512);u.GetWindowTextW(h,buf,512)
  if 'AIExample Preview' in buf.value:windows.append((h,buf.value))
 return True
u.EnumWindows(cb,0)
print(windows)
if len(sys.argv)>1:
 key=int(sys.argv[1],0);idx=int(sys.argv[2]) if len(sys.argv)>2 else 0
 h=windows[idx][0]
 u.GetForegroundWindow.restype=wintypes.HWND
 u.GetWindowRect.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.RECT)]
 u.keybd_event(0x12,0,0,0);u.keybd_event(0x12,0,2,0)
 focused=u.SetForegroundWindow(h);time.sleep(.3)
 print('FOREGROUND',focused,u.GetForegroundWindow(),h)
 if len(sys.argv)>3 and sys.argv[3]=='click':
  rect=wintypes.RECT();u.GetWindowRect(h,ctypes.byref(rect));u.SetCursorPos((rect.left+rect.right)//2,(rect.top+rect.bottom)//2)
  u.mouse_event(2,0,0,0,0);time.sleep(.1);u.mouse_event(4,0,0,0,0);time.sleep(.3)
 u.keybd_event(key,0,0,0);time.sleep(.15);u.keybd_event(key,0,2,0);time.sleep(.5)



