import unreal,json,time,traceback
from pathlib import Path
worlds=unreal.EditorLevelLibrary.get_pie_worlds(False)
sw=next(w for w in worlds if unreal.GameplayStatics.get_player_pawn(w,0).has_authority());cw=next(w for w in worlds if not unreal.GameplayStatics.get_player_pawn(w,0).has_authority())
hpc=unreal.GameplayStatics.get_player_controller(sw,0);cpc=unreal.GameplayStatics.get_player_controller(cw,0)
rpc=next(p.get_controller() for p in unreal.GameplayStatics.get_all_actors_of_class(sw,unreal.Pawn) if not p.is_locally_controlled())
hi=hpc.get_editor_property('InventoryComponent');ci=cpc.get_editor_property('InventoryComponent');ri=rpc.get_editor_property('InventoryComponent')
rp=rpc.get_controlled_pawn();cp=cpc.get_controlled_pawn();hp=hpc.get_controlled_pawn()
report={'checks':{},'mode':'two-player listen-server PIE'};state={'phase':0,'next':time.monotonic()+1}
def a(i,n):return list(i.get_editor_property(n))
def v(i):return i.get_editor_property('LayoutVersion')
def check(n,b):
 report['checks'][n]=bool(b)
 assert b,n
def active(i):return i.get_editor_property('ActiveWeaponInstance')
def slot(p):return p.get_editor_property('PublicActiveSlot')
def visual(p,n):return p.get_editor_property(n)
def transfer(uid,target):
 loc=next(n for n in range(11) if ri.call_method('GetInstanceAtLocation',(n,))==uid)
 assert ri.call_method('TryTransferWeapon',(loc,target,uid,v(ri)))
def select(s):ri.call_method('TrySelectWeapon',(s,a(ri,'EquipmentInstances')[s],v(ri)))
def finish():
 report['passed']=all(report['checks'].values()) and 'error' not in report
 (Path(unreal.Paths.project_saved_dir())/'WeaponSwitchValidation/runtime-result.json').write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(weapon_test_handle)
def tick(dt):
 if time.monotonic()<state['next']:return
 try:
  phase=state['phase']
  if phase==0:
   check('initially_holstered',slot(hp)==slot(cp)==slot(rp)==-1)
   for definition,mag,count in [('DA_PistolItem',6,2),('DA_EquipmentTestLongGun',17,2)]:
    d=unreal.load_asset('/Game/AIExample/Items/'+definition);f=unreal.new_object(d.get_class())
    for k in ['ItemID','Category','EquipmentType','MaxStackSize']:f.set_editor_property(k,d.get_editor_property(k))
    f.set_editor_property('InitialMagazine',mag);assert ri.call_method('TryAddItem',(f,count))
   state['ids']=a(ri,'WeaponInstances');p1,p2,l1,l2=state['ids']
   transfer(p1,10);transfer(l1,8);transfer(l2,9)
  elif phase==1:
   check('equipped_ids_publicly_replicate',str(cp.get_editor_property('PublicSidearm'))=='Weapon.Pistol' and str(cp.get_editor_property('PublicPrimary'))=='Weapon.TestLongGun')
   check('stowed_visuals_visible',all(not visual(cp,n).get_editor_property('hidden_in_game') for n in ['PrimaryVisual','SecondaryVisual','SidearmVisual']))
   check('cosmetic_collision_disabled',all(visual(cp,n).get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and not visual(cp,n).is_simulating_physics() for n in ['PrimaryVisual','SecondaryVisual','SidearmVisual']))
   check('direct_client_select_rejected',not ci.call_method('TrySelectWeapon',(2,a(ci,'EquipmentInstances')[2],v(ci))))
   select(2)
  elif phase==2:
   check('server_selection_replicates_pistol',active(ri)==active(ci)==state['ids'][0] and slot(rp)==slot(cp)==2)
   check('pistol_attached_to_hand',str(visual(cp,'SidearmVisual').get_attach_socket_name())=='hand_r')
   check('owner_inventory_private',len(unreal.GameplayStatics.get_all_actors_of_class(cw,cpc.get_class()))==1)
   select(0)
  elif phase==3:
   check('switch_to_primary',slot(cp)==slot(rp)==0 and active(ri)==state['ids'][2])
   check('pistol_holsters_when_switched',str(visual(cp,'SidearmVisual').get_attach_socket_name())=='pelvis')
   select(1)
  elif phase==4:
   check('switch_to_secondary',slot(cp)==slot(rp)==1 and active(ri)==state['ids'][3]);select(1)
  elif phase==5:
   check('same_key_holsters',slot(cp)==slot(rp)==-1 and active(ri)=='')
   select(2)
  elif phase==6:
   before=active(ri)
   check('stale_version_rejected',not ri.call_method('TrySelectWeapon',(0,state['ids'][2],v(ri)-1)) and active(ri)==before)
   check('wrong_instance_rejected',not ri.call_method('TrySelectWeapon',(0,state['ids'][0],v(ri))) and active(ri)==before)
   check('invalid_slot_rejected',all(not ri.call_method('TrySelectWeapon',(s,before,v(ri))) for s in [-1,3,999]))
   transfer(state['ids'][1],10)
  elif phase==7:
   check('swapping_active_weapon_holsters',active(ri)==active(ci)=='' and slot(cp)==-1)
   select(2)
  elif phase==8:
   check('replacement_can_be_drawn',active(ri)==state['ids'][1]);transfer(state['ids'][1],-1)
  elif phase==9:
   check('unequipping_active_weapon_clears_visual',active(ri)=='' and slot(cp)==-1 and visual(cp,'SidearmVisual').get_editor_property('hidden_in_game'))
   select(0)
  elif phase==10:
   check('empty_slot_keeps_current_weapon',not ri.call_method('TrySelectWeapon',(2,'',v(ri))) and active(ri)==state['ids'][2])
   transfer(state['ids'][2],9)
  elif phase==11:
   check('active_instance_follows_equipment_swap',active(ri)==state['ids'][2] and slot(cp)==slot(rp)==1)
   cpc.call_method('ToggleInventory');cpc.call_method('RequestSelectWeapon',(0,))
  elif phase==12:
   check('inventory_blocks_switching',slot(cp)==1);cpc.call_method('CloseInventory')
   check('magazines_unchanged',a(ci,'WeaponMagazines')==a(ri,'WeaponMagazines')==[6,6,17,17])
   check('all_instances_conserved',sorted(x for x in a(ri,'BackpackInstances')+a(ri,'EquipmentInstances') if x)==sorted(state['ids']))
   check('host_remains_independent',not a(hi,'WeaponInstances') and slot(hp)==-1)
   # Equip pistol again for physical input and visual review.
   transfer(state['ids'][0],10)
   finish();return
  state['phase']+=1;state['next']=time.monotonic()+.8
 except Exception:report['error']=traceback.format_exc();finish()
weapon_test_handle=unreal.register_slate_post_tick_callback(tick)


