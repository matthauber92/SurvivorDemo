Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class InventoryUIWindow {
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern void keybd_event(byte key,byte scan,uint flags,UIntPtr extra);
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h,out RECT rect);
 [DllImport("user32.dll")] public static extern bool SetCursorPos(int x,int y);
 [DllImport("user32.dll")] public static extern void mouse_event(uint flags,uint x,uint y,uint data,UIntPtr extra);
 public struct RECT { public int Left,Top,Right,Bottom; }
}
"@
$projectFile = Join-Path $PSScriptRoot '../AIExample.uproject'
$reportDir = Join-Path $PSScriptRoot '../Saved/InventoryUIValidation'
$gameProcess = Start-Process -FilePath 'C:\Users\Matt Hauber\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe' -ArgumentList @(('"'+(Resolve-Path $projectFile).Path+'"'),'/Game/AIExample/Maps/Lvl_PickupTest','-game','-windowed','-ResX=1280','-ResY=800','-NoSplash','-log=InventoryStandalone.log') -WindowStyle Hidden -PassThru
try {
 for ($attempt=0; $attempt -lt 50; $attempt++) {
  Start-Sleep -Milliseconds 800
  $gameProcess.Refresh()
  if ($gameProcess.HasExited) { throw 'Standalone exited before window creation' }
  if ($gameProcess.MainWindowHandle -ne [IntPtr]::Zero) { break }
 }
 Start-Sleep -Seconds 4
 $gameWindow=$gameProcess.MainWindowHandle
 if ($gameWindow -eq [IntPtr]::Zero) { throw 'No standalone window' }
 [InventoryUIWindow]::keybd_event(18,0,0,[UIntPtr]::Zero)
 [InventoryUIWindow]::keybd_event(18,0,2,[UIntPtr]::Zero)
 [void][InventoryUIWindow]::SetForegroundWindow($gameWindow)
 Start-Sleep -Milliseconds 500
 $rect=New-Object InventoryUIWindow+RECT
 [void][InventoryUIWindow]::GetWindowRect($gameWindow,[ref]$rect)
 [void][InventoryUIWindow]::SetCursorPos(($rect.Left+$rect.Right)/2,($rect.Top+$rect.Bottom)/2)
 [InventoryUIWindow]::mouse_event(2,0,0,0,[UIntPtr]::Zero)
 [InventoryUIWindow]::mouse_event(4,0,0,0,[UIntPtr]::Zero)
 function Press-Key([byte]$key) {
  [InventoryUIWindow]::keybd_event($key,0,0,[UIntPtr]::Zero)
  Start-Sleep -Milliseconds 120
  [InventoryUIWindow]::keybd_event($key,0,2,[UIntPtr]::Zero)
  Start-Sleep -Milliseconds 600
 }
 function Capture-Game([string]$name) {
  [void][InventoryUIWindow]::GetWindowRect($gameWindow,[ref]$rect)
  $bitmap=New-Object System.Drawing.Bitmap(($rect.Right-$rect.Left),($rect.Bottom-$rect.Top))
  $graphics=[System.Drawing.Graphics]::FromImage($bitmap)
  $graphics.CopyFromScreen($rect.Left,$rect.Top,0,0,$bitmap.Size)
  $bitmap.Save((Join-Path $reportDir $name),[System.Drawing.Imaging.ImageFormat]::Png)
  $graphics.Dispose();$bitmap.Dispose()
 }
 Press-Key 69
 Press-Key 73
 Capture-Game 'standalone-I-open.png'
 Press-Key 73
 Capture-Game 'standalone-I-close.png'
 Press-Key 73
 Press-Key 27
 Capture-Game 'standalone-Escape-close.png'
 Write-Output 'Standalone screenshots captured for I open, I close, and Escape close.'
} finally {
 if (-not $gameProcess.HasExited) { [void]$gameProcess.CloseMainWindow() }
}
