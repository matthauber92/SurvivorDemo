from pathlib import Path
s=Path('MigrationStaging/test_shoulder_controls.py').read_text()
s=s.replace("w=unreal.EditorLevelLibrary.get_pie_worlds(False)[0]", "w=next(w for w in unreal.EditorLevelLibrary.get_pie_worlds(False) if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())")
s=s.replace("'AIExample Preview' in b.value", "'AIExample Preview' in b.value and 'Client' in b.value")
s=s.replace('controls-result.json','client-controls-result.json').replace('physical mouse and keyboard in standalone PIE','physical mouse and keyboard in remote-client PIE')
start=s.index(' run("p.set_actor_location(unreal.Vector(-1500,-1500,88)')
end=s.index(" report['passed']=True",start)
s=s[:start]+s[end:]
Path('MigrationStaging/test_client_shoulder_controls.py').write_text(s)
