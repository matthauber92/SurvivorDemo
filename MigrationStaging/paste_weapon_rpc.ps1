Add-Type @"
using System; using System.Runtime.InteropServices;
public static class InventoryPasteUI {
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h,out RECT r);
 [DllImport("user32.dll")] public static extern bool SetCursorPos(int x,int y);
 [DllImport("user32.dll")] public static extern void mouse_event(uint f,uint x,uint y,uint d,UIntPtr e);
 [DllImport("user32.dll")] public static extern void keybd_event(byte k,byte s,uint f,UIntPtr e);
 public struct RECT { public int Left,Top,Right,Bottom; }
}
"@
$editorProcess=Get-Process UnrealEditor | Select-Object -First 1
$window=$editorProcess.MainWindowHandle
if ($window -eq 0) { $window=[InventoryPasteUI]::GetForegroundWindow() }
[InventoryPasteUI]::keybd_event(18,0,0,[UIntPtr]::Zero)
[InventoryPasteUI]::keybd_event(18,0,2,[UIntPtr]::Zero)
[void][InventoryPasteUI]::SetForegroundWindow($window)
$bounds=New-Object InventoryPasteUI+RECT
[void][InventoryPasteUI]::GetWindowRect($window,[ref]$bounds)
function Click-Ratio([double]$x,[double]$y) {
 [void][InventoryPasteUI]::SetCursorPos(($bounds.Left+($bounds.Right-$bounds.Left)*$x),($bounds.Top+($bounds.Bottom-$bounds.Top)*$y))
 [InventoryPasteUI]::mouse_event(2,0,0,0,[UIntPtr]::Zero)
 [InventoryPasteUI]::mouse_event(4,0,0,0,[UIntPtr]::Zero)
 Start-Sleep -Milliseconds 400
}
$oldClipboard=Get-Clipboard -Raw
try {
 Set-Clipboard -Value (Get-Content (Join-Path $PSScriptRoot 'weapon-rpc-node.txt') -Raw)
 Click-Ratio .21 .04
 Click-Ratio .35 .108
 Click-Ratio .5 .45
 [InventoryPasteUI]::keybd_event(17,0,0,[UIntPtr]::Zero)
 [InventoryPasteUI]::keybd_event(86,0,0,[UIntPtr]::Zero)
 [InventoryPasteUI]::keybd_event(86,0,2,[UIntPtr]::Zero)
 [InventoryPasteUI]::keybd_event(17,0,2,[UIntPtr]::Zero)
 Start-Sleep -Milliseconds 700
} finally { Set-Clipboard -Value $oldClipboard }



