param([int]$X = -1, [int]$Y = -1, [string]$Keys = '', [string]$TextFile = '', [switch]$RightClick, [switch]$MeshTab, [string]$Screenshot = '', [string]$StepsFile = '')
Add-Type -AssemblyName System.Windows.Forms
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class InteractionUI { [DllImport("user32.dll")] public static extern bool SetProcessDPIAware(); [DllImport("user32.dll")] public static extern int GetSystemMetrics(int n); [DllImport("user32.dll")] public static extern bool SetCursorPos(int x,int y); [DllImport("user32.dll")] public static extern void mouse_event(uint f,uint x,uint y,uint d,UIntPtr e); }'
[InteractionUI]::SetProcessDPIAware() | Out-Null
$displayScale = [InteractionUI]::GetSystemMetrics(0) / 1280.0
if ($MeshTab) {
 [InteractionUI]::SetCursorPos([int](272*$displayScale),[int](26*$displayScale)) | Out-Null
 [InteractionUI]::mouse_event(2,0,0,0,[UIntPtr]::Zero)
 [InteractionUI]::mouse_event(4,0,0,0,[UIntPtr]::Zero)
 Start-Sleep -Milliseconds 500
}
if ($X -ge 0) {
    [InteractionUI]::SetCursorPos([int]($X * $displayScale), [int]($Y * $displayScale)) | Out-Null
    if ($RightClick) { [InteractionUI]::mouse_event(8,0,0,0,[UIntPtr]::Zero); [InteractionUI]::mouse_event(16,0,0,0,[UIntPtr]::Zero) }
    else { [InteractionUI]::mouse_event(2,0,0,0,[UIntPtr]::Zero); [InteractionUI]::mouse_event(4,0,0,0,[UIntPtr]::Zero) }
    Start-Sleep -Milliseconds 150
}
if ($TextFile) { Set-Clipboard -Value (Get-Content -LiteralPath $TextFile -Raw); [System.Windows.Forms.SendKeys]::SendWait('^v') }
if ($Keys) { [System.Windows.Forms.SendKeys]::SendWait($Keys) }
if ($StepsFile) {
 foreach ($step in (Get-Content -LiteralPath $StepsFile -Raw | ConvertFrom-Json)) {
  if ($step.x -ne $null) { [InteractionUI]::SetCursorPos([int]($step.x*$displayScale),[int]($step.y*$displayScale)) | Out-Null }
  if ($step.action -eq 'click') { [InteractionUI]::mouse_event(2,0,0,0,[UIntPtr]::Zero); [InteractionUI]::mouse_event(4,0,0,0,[UIntPtr]::Zero) }
  if ($step.action -eq 'right') { [InteractionUI]::mouse_event(8,0,0,0,[UIntPtr]::Zero); [InteractionUI]::mouse_event(16,0,0,0,[UIntPtr]::Zero) }
  if ($step.action -eq 'paste') { Set-Clipboard -Value $step.text; [System.Windows.Forms.SendKeys]::SendWait('^a'); [System.Windows.Forms.SendKeys]::SendWait('^v') }
  Start-Sleep -Milliseconds 600
 }
}
Start-Sleep -Milliseconds 1000
if ($Screenshot) {
 Add-Type -AssemblyName System.Drawing
 $b=New-Object System.Drawing.Bitmap([InteractionUI]::GetSystemMetrics(0),[InteractionUI]::GetSystemMetrics(1))
 $g=[System.Drawing.Graphics]::FromImage($b)
 $g.CopyFromScreen(0,0,0,0,$b.Size)
 $b.Save($Screenshot)
 $g.Dispose(); $b.Dispose()
}
