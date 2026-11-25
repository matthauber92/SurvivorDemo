import unreal
from pathlib import Path
from editor_toolset.toolsets.object import ObjectTools as O
for path in ['/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/CHT_PoseSearchDatabases_Dense','/Game/Characters/UEFN_Mannequin/Animations/ExperimentalStateMachineData/CHT_CMCCharacterAnimations']:
 c=unreal.load_asset(path)
 (Path(unreal.Paths.project_saved_dir())/'LocomotionRepair'/(c.get_name()+'.json')).write_text(O.get_properties(c,['ContextData','ColumnsStructs']))
 print(c.get_name(),[n for n in dir(c) if 'compile' in n.lower()])
