import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
R='/Game/AIExample/';out=Path(unreal.Paths.project_saved_dir())/'WeaponSwitchValidation'
paths=['Items/BP_InventoryComponent','Items/BP_InventoryPlayerController','Interaction/BP_SurvivorInteractionCharacter','Interaction/IMC_SurvivorInteraction','Interaction/IA_SelectPrimary','Interaction/IA_SelectSecondary','Interaction/IA_SelectSidearm']
settings=unreal.ValidateAssetsSettings(validation_usecase=unreal.DataValidationUsecase.COMMANDLET,collect_per_asset_details=True)
ret,res=unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem).validate_assets_with_settings([unreal.EditorAssetLibrary.find_asset_data(R+p) for p in paths],settings)
stats={n:res.get_editor_property(n) for n in ['num_checked','num_valid','num_invalid','num_warnings']}
assert stats['num_invalid']==stats['num_warnings']==0,stats
reports={n:json.loads((out/(n+'-result.json')).read_text()) for n in ['runtime','keyboard','observer','disk']}
assert all(r['passed'] for r in reports.values()),reports
report={'milestone':'5B: equipped weapon drawing, holstering, switching and replication','passed':True,'controls':{'1':'Primary','2':'Secondary','3':'Sidearm','active slot key':'Holster'},'assets':paths,'validation':stats,'test_reports':reports,'limitations':['Instant attachment changes; dedicated draw/holster and gripping animations are not implemented.','Long guns use scaled cube placeholders.','Aiming, firing and reloading are the next milestone.','Network validation used two-player listen-server PIE, not a 14-player load test.'],'backup':'Backups/BeforeMilestone5B-20261117-112347/AIExample'}
(out/'milestone5b-report.json').write_text(json.dumps(report,indent=2))
(out/'final-graphs.json').write_text(json.dumps({p:{g.get_name():B.read_graph_dsl(g) for g in B.list_graphs(unreal.load_asset(R+p))} for p in paths[:3]},indent=2))
print('WEAPON_MILESTONE_PASS',stats,sum(len(r['checks']) for r in reports.values()))
