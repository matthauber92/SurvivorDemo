"""Targeted camera defaults and interaction trace limits; preserves socket edits."""
import unreal,shutil,datetime
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as B
from editor_toolset.toolsets.actor import ActorTools as A
assert not unreal.EditorLevelLibrary.get_pie_worlds(False)
root=Path(unreal.Paths.project_dir()).resolve()
backup=root/'Backups'/('CameraPickup-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir(parents=True)
paths=['Interaction/BP_SurvivorInteractionCharacter','Interaction/BP_InteractionComponent']
for path in paths:shutil.copy2(root/'Content/AIExample'/(path+'.uasset'),backup/(path.split('/')[-1]+'.uasset'))
bp=unreal.load_asset('/Game/AIExample/'+paths[0]);d=B.get_default_object(bp)
d.set_editor_property('CameraWalkDistance',250.0)
boom=next(c for c in A.get_components(d) if c.get_name()=='ShoulderBoom_GEN_VARIABLE')
boom.set_editor_property('target_arm_length',250.0)
assert unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
comp=unreal.load_asset('/Game/AIExample/'+paths[1])
# Change only constant pins, keeping the existing interface calls, RPCs and hit outputs.
changed=[]
for name in ['ValidateTarget','UpdateFocus']:
 for n in B.find_nodes(B.get_graph(comp,name)):
  for pin in B._get_node_info(n).input_pins:
   if pin.connected_pins:continue
   if pin.value in ['500.0','500.000000','500'] and name=='ValidateTarget':
    B.set_pin_value(pin.pin_id,'850.0');changed.append((name,pin.name,500,850))
   elif pin.value in ['750.0','750.000000','750']:
    B.set_pin_value(pin.pin_id,'1100.0');changed.append((name,pin.name,750,1100))
assert len(changed)>=3,changed
B.compile_blueprint(comp,warnings_as_errors=True)
assert unreal.EditorAssetLibrary.save_loaded_asset(comp,only_if_is_dirty=False)
print('CAMERA_DISTANCE',d.get_editor_property('CameraWalkDistance'),'PICKUP_LIMITS',changed,'BACKUP',str(backup))

