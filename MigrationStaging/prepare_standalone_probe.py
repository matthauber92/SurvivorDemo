from pathlib import Path
p=Path('MigrationStaging/test_inventory_standalone_process.ps1');s=p.read_text().replace('-WindowStyle Hidden','-WindowStyle Normal')
s=s.replace("'-log=InventoryStandalone.log'","'-log=InventoryStandalone.log',('-ExecCmds="+'"'+"py " + '"' + "'+(Join-Path $PSScriptRoot 'probe_standalone_game.py')+'" + '"' + "')")
Path('MigrationStaging/test_inventory_standalone_probe.ps1').write_text(s)
