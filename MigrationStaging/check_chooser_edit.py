import unreal
c=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/CHT_PoseSearchDatabases')
v=c.get_editor_property('context_data')[0];print('BEFORE',v.export_text());r=v.import_text(v.export_text().replace('/Game/Blueprints/SandboxCharacter_CMC_ABP.SandboxCharacter_CMC_ABP_C','/Game/AIExample/Combat/Animation/ABP_SurvivorCombat.ABP_SurvivorCombat_C'));print('RETURN',r,'AFTER',v.export_text())
