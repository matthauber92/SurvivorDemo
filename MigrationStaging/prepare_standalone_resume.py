from pathlib import Path
p=Path('MigrationStaging/test_inventory_standalone_process.ps1');s=p.read_text()
s=s.replace('public static class InventoryUIWindow {','''public static class InventoryUIWindow {
 public delegate bool EnumProc(IntPtr h,IntPtr p);
 [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb,IntPtr p);
 [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h,out uint pid);
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int mode);
 public static void Reveal(uint target) { EnumWindows((h,p)=>{uint pid; GetWindowThreadProcessId(h,out pid); if(pid==target){ RECT r; GetWindowRect(h,out r); if(r.Right-r.Left>500 && r.Bottom-r.Top>400) ShowWindow(h,5); } return true;},IntPtr.Zero); }
''')
a=s.index('$gameProcess = Start-Process');b=s.index('\ntry {',a)
s=s[:a]+'''$gameProcess = Get-Process -Id 2444
[InventoryUIWindow]::Reveal(2444)
'''+s[b:]
p=Path('MigrationStaging/resume_inventory_standalone_process.ps1');p.write_text(s)
