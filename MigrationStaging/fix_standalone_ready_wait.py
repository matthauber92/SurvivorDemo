from pathlib import Path
p=Path('MigrationStaging/test_inventory_standalone_probe.ps1');s=p.read_text().replace('Start-Sleep -Seconds 8', '''for ($probeWait=0; $probeWait -lt 60; $probeWait++) {
  if (Test-Path (Join-Path $reportDir 'standalone-probe.json')) { break }
  Start-Sleep -Milliseconds 800
 }
 if (-not (Test-Path (Join-Path $reportDir 'standalone-probe.json'))) { throw 'Runtime probe did not become ready' }
 $gameProcess.Refresh()
 Start-Sleep -Seconds 1''')
p.write_text(s)
