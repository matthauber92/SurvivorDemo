import unreal
c=unreal.load_asset('/Game/AIExample/Combat/Animation/CHT_PoseSearchDatabases')
for n in ['ResultsStructs','results_structs','CookedResults','FallbackResult','NestedChoosers']:
 try:print(n,c.get_editor_property(n))
 except Exception as e:print(n,str(e))
