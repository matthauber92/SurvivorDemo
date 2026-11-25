from pathlib import Path
p=Path('MigrationStaging/test_inventory_standalone_probe.ps1');s=p.read_text();lines=s.splitlines()
for i,line in enumerate(lines):
 if line.startswith('$gameProcess = Start-Process'):
  lines[i]="""$gameProcess = Start-Process -FilePath 'C:\\Users\\Matt Hauber\\Epic Games\\UE_5.8\\Engine\\Binaries\\Win64\\UnrealEditor.exe' -ArgumentList @(('"'+(Resolve-Path $projectFile).Path+'"'),'/Game/AIExample/Maps/Lvl_PickupTest','-game','-windowed','-ResX=1280','-ResY=800','-NoSplash','-log=InventoryStandalone.log','-ExecCmds="py exec(open(unreal.Paths.project_dir()+''MigrationStaging/probe_standalone_game.py'').read())"') -WindowStyle Normal -PassThru"""
s='\n'.join(lines).replace('Start-Sleep -Seconds 4','Start-Sleep -Seconds 8');p.write_text(s)
p=Path('MigrationStaging/probe_standalone_game.py');s=p.read_text().replace("report[w.get_path_name()]['widget']=str(widget)","report[w.get_path_name()]['widget']=str(widget)\n    pc.call_method('CloseInventory')");p.write_text(s)
