param([switch]$PressE,[switch]$AimOpenDoor,[switch]$AimPickup)
Add-Type -AssemblyName System.Windows.Forms
Add-Type -TypeDefinition @'
using System;
using System.Text;
using System.Runtime.InteropServices;
public class InteractionKeyboard {
 public delegate bool EnumProc(IntPtr h,IntPtr p);
 [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc p,IntPtr l);
 [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h,StringBuilder s,int n);
 [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern void keybd_event(byte vk,byte scan,uint flags,UIntPtr extra);
 public struct Rect {public int left,top,right,bottom;}
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h,out Rect r);
 [DllImport("user32.dll")] public static extern bool SetCursorPos(int x,int y);
 [DllImport("user32.dll")] public static extern void mouse_event(uint f,uint x,uint y,uint d,UIntPtr e);
}
'@
$script:gameWindows = @()
[InteractionKeyboard]::EnumWindows({param($h,$p)
 $title = New-Object System.Text.StringBuilder 512
 [void][InteractionKeyboard]::GetWindowText($h,$title,512)
 if ([InteractionKeyboard]::IsWindowVisible($h) -and $title.ToString() -match 'AIExample.*Preview') {
  $script:gameWindows += [PSCustomObject]@{Handle=$h;Title=$title.ToString()}
 }
 return $true
},[IntPtr]::Zero) | Out-Null
$gameWindows | Format-Table
if ($PressE) {
 if ($gameWindows.Count -ne 1) { throw 'Expected exactly one floating PIE game window.' }
 if (-not [InteractionKeyboard]::SetForegroundWindow($gameWindows[0].Handle)) { throw 'Could not focus game window.' }
 Start-Sleep -Milliseconds 500
 $rect = New-Object InteractionKeyboard+Rect
 [void][InteractionKeyboard]::GetWindowRect($gameWindows[0].Handle,[ref]$rect)
 [void][InteractionKeyboard]::SetCursorPos(($rect.left+$rect.right)/2,($rect.top+$rect.bottom)/2)
 [InteractionKeyboard]::mouse_event(2,0,0,0,[UIntPtr]::Zero)
 [InteractionKeyboard]::mouse_event(4,0,0,0,[UIntPtr]::Zero)
 Start-Sleep -Milliseconds 300
 if ($AimOpenDoor) {
  & 'C:/Users/Matt Hauber/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe' MigrationStaging/run_editor_script.py MigrationStaging/aim_client_open_door.py
  Start-Sleep -Milliseconds 500
 }
 if ($AimPickup) {
  & 'C:/Users/Matt Hauber/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe' MigrationStaging/run_editor_script.py MigrationStaging/aim_client_pickup.py
  Start-Sleep -Milliseconds 500
 }
 [InteractionKeyboard]::keybd_event(0x45,0,0,[UIntPtr]::Zero)
 Start-Sleep -Milliseconds 150
 [InteractionKeyboard]::keybd_event(0x45,0,2,[UIntPtr]::Zero)
 Start-Sleep -Milliseconds 700
}
