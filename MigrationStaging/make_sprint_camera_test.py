from pathlib import Path
s=Path('MigrationStaging/test_shoulder_controls.py').read_text();a=s.index(" check('idle_crosshair_hidden'");b=s.index('\nexcept Exception:')
body='''
 run("p.set_actor_location(unreal.Vector(-1200,0,88),False,True);pc.set_control_rotation(unreal.Rotator())")
 u.keybd_event(0x57,0x11,0,0);time.sleep(.5);u.keybd_event(0xA0,0x2A,0,0);time.sleep(1.7)
 print(run("print('STATE',p.get_editor_property('CharacterInputState'),p.get_velocity(),p.get_editor_property('ShoulderBoom').get_editor_property('target_arm_length'),p.get_actor_location())"),flush=True)
 print('ARM',ev("p.get_editor_property('ShoulderBoom').get_editor_property('target_arm_length')"),flush=True)
 check('sprint_camera_pulls_back',ev("p.get_editor_property('ShoulderBoom').get_editor_property('target_arm_length')")>590)
 check('sprint_crosshair_hidden',not ev("p.get_editor_property('ShouldShowCrosshair')"))
 run("unreal.SystemLibrary.execute_console_command(w,'Shot',pc)")
 u.keybd_event(0x57,0x11,2,0);u.keybd_event(0xA0,0x2A,2,0);time.sleep(1.5)
 check('stopping_restores_close_camera',abs(ev("p.get_editor_property('ShoulderBoom').get_editor_property('target_arm_length')")-350)<2)
 report['passed']=True'''
s=s[:a]+body+s[b:];s=s.replace('controls-result.json','sprint-result.json').replace('u.keybd_event(0x10,0,2,0)','u.keybd_event(0xA0,0x2A,2,0)')
Path('MigrationStaging/test_sprint_camera.py').write_text(s)
