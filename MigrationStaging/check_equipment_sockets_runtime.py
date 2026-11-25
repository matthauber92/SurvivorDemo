import unreal,time,json,traceback
from pathlib import Path
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
sw=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority());cw=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
p=unreal.GameplayStatics.get_player_pawn(sw,0);pc=p.get_controller();i=pc.get_editor_property('InventoryComponent')
observer=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(cw,p.get_class()) if not a.is_locally_controlled())
report={'checks':{}};state={'phase':0,'next':time.monotonic()+.5}
def check(n,b):report['checks'][n]=bool(b);assert b,n
def finish():
 report['passed']=all(report['checks'].values()) and 'error' not in report
 (Path(unreal.Paths.project_saved_dir())/'EquipmentSocketValidation/runtime.json').write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(socket_check_handle)
def select(slot):assert i.call_method('TrySelectWeapon',(slot,i.get_editor_property('EquipmentInstances')[slot],i.get_editor_property('LayoutVersion')))
def placement(label,expected):
 for actor,role in [(p,'server'),(observer,'observer')]:
  for name,socket in expected.items():
   c=actor.get_editor_property(name)
   check(label+'_'+role+'_'+name,str(c.get_attach_socket_name())==socket and not c.get_editor_property('hidden_in_game'))
   check(label+'_'+role+'_'+name+'_no_offsets',c.get_editor_property('relative_location').length()<.01 and all(abs(getattr(c.get_editor_property('relative_rotation'),a))<.01 for a in ['pitch','yaw','roll']))
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   for definition,count in [('DA_PistolItem',1),('DA_EquipmentTestLongGun',2)]:assert i.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/'+definition),count))
   ids=list(i.get_editor_property('WeaponInstances'))
   for uid,target in zip(ids,[10,8,9]):
    source=next(n for n in range(8) if i.call_method('GetInstanceAtLocation',(n,))==uid)
    assert i.call_method('TryTransferWeapon',(source,target,uid,i.get_editor_property('LayoutVersion')))
  elif phase==1:
   placement('holstered',{'PrimaryVisual':'PrimaryHolster','SecondaryVisual':'SecondaryHolster','SidearmVisual':'PistolHolster'});select(2)
  elif phase==2:
   placement('pistol_drawn',{'SidearmVisual':'PistolGrip_R'});select(0)
  elif phase==3:
   placement('primary_drawn',{'PrimaryVisual':'LongGunGrip_R','SidearmVisual':'PistolHolster'});select(1)
  elif phase==4:
   placement('secondary_drawn',{'SecondaryVisual':'LongGunGrip_R','PrimaryVisual':'PrimaryHolster'});select(1)
  elif phase==5:
   placement('holstered_again',{'SecondaryVisual':'SecondaryHolster'})
   check('all_instances_preserved',len(i.get_editor_property('WeaponInstances'))==3 and len([x for x in i.get_editor_property('EquipmentInstances') if x])==3)
   finish();return
  state['phase']+=1;state['next']=time.monotonic()+.7
 except Exception:report['error']=traceback.format_exc();finish()
socket_check_handle=unreal.register_slate_post_tick_callback(tick)
