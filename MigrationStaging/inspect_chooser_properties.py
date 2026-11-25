import unreal
from editor_toolset.toolsets.object import ObjectTools as O
c=unreal.load_asset('/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/CHT_PoseSearchDatabases')
print(O.list_properties(c))
print(O.get_properties(c,['ContextData','ResultsStructs','NestedChoosers','FallbackResult','ColumnsStructs']))
