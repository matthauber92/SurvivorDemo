import unreal
ed=unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
ed.close_all_editors_for_asset(unreal.load_asset('/Game/AIExample/Combat/NS_BulletImpact'))
ed.open_editor_for_assets([unreal.load_asset('/Game/AIExample/Weapons/TheHouse/07_ParticleFX/Pistol/NS_Pistol')])
