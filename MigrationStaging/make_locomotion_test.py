from pathlib import Path
s=Path('MigrationStaging/test_pistol_keyboard.py').read_text();start=s.index(' key(0x33,1.6);check');end=s.index('\nexcept Exception:')
body='''
 run("a=p.get_component_by_class(unreal.SkeletalMeshComponent).get_anim_instance();p.set_actor_location(unreal.Vector(-1500,-900,88),False,True);pc.set_control_rotation(unreal.Rotator())")
 def selected():return ev("a.get_editor_property('CurrentSelectedAnim').get_name()")
 def falling():return ev("p.get_component_by_class(unreal.CharacterMovementComponent).is_falling()")
 def snap(name):
  report.setdefault('samples',{})[name]={'animation':selected(),'falling':falling(),'speed':ev("a.get_editor_property('Speed2D')")}
 def jump_check(prefix):
  u.keybd_event(0x20,0x39,0,0);time.sleep(.08);u.keybd_event(0x20,0x39,2,0);time.sleep(.22)
  snap(prefix+'_air');check(prefix+'_airborne',falling());check(prefix+'_jump_animation','Jump' in selected() or 'Fall' in selected())
  run("unreal.SystemLibrary.execute_console_command(w,'Shot',pc)")
  time.sleep(1.5);snap(prefix+'_landed');check(prefix+'_landed',not falling());check(prefix+'_idle_after_landing','Idle' in selected())
 time.sleep(1.2);snap('unarmed_idle');check('unarmed_idle_animation','Idle' in selected())
 jump_check('unarmed_jump')
 u.keybd_event(0x57,0x11,0,0);time.sleep(1.1);snap('moving');check('moving_locomotion','Idle' not in selected() and not falling())
 u.keybd_event(0x57,0x11,2,0);time.sleep(1.6);snap('stopped');check('stop_returns_idle','Idle' in selected())
 run("inv.call_method('TryAddItem',(unreal.load_asset('/Game/AIExample/Items/DA_PistolItem'),1));uid=inv.get_editor_property('BackpackInstances')[0];inv.call_method('TryTransferWeapon',(0,10,uid,inv.get_editor_property('LayoutVersion')))")
 key(0x33,1.6);snap('armed_idle');check('armed_idle_locomotion','Idle' in selected());check('pistol_layer_active',ev("a.get_editor_property('PistolLayerWeight')")>.99)
 jump_check('armed_jump')
 u.mouse_event(8,0,0,0,0);time.sleep(.6);snap('aim_idle');check('aiming_keeps_idle','Idle' in selected());check('aim_crosshair_preserved',ev("p.get_editor_property('ShouldShowCrosshair')"));u.mouse_event(16,0,0,0,0)
 key(0x33,.6);check('holstering_removes_pistol_layer',ev("a.get_editor_property('PistolLayerWeight')")<.01)
 report['passed']=True'''
s=s[:start]+body+s[end:];s=s.replace('Saved/PistolCombatValidation/keyboard-result.json','Saved/LocomotionRepair/controls-result.json')
s=s.replace('u.mouse_event(4,0,0,0,0);u.mouse_event(16,0,0,0,0);r.stop()','u.keybd_event(0x57,0x11,2,0);u.keybd_event(0x20,0x39,2,0);u.mouse_event(4,0,0,0,0);u.mouse_event(16,0,0,0,0);r.stop()')
Path('MigrationStaging/test_locomotion_controls.py').write_text(s)
