import unreal,json,builtins
from pathlib import Path
keyboard_record_handle,keyboard_samples,keyboard_doors=builtins.interaction_keyboard_record
unreal.unregister_slate_post_tick_callback(keyboard_record_handle)
open_edges=[i for i in range(1,len(keyboard_samples)) if not keyboard_samples[i-1]['doors'][0]['open'] and keyboard_samples[i]['doors'][0]['open']]
if open_edges:keyboard_samples=keyboard_samples[max(0,open_edges[-1]-1):]
checks={}
for i,d in enumerate(keyboard_doors):
    label='server' if d.has_authority() else 'client'
    values=[s['doors'][i] for s in keyboard_samples]
    checks[label+'_opened_with_real_E']=any(v['open'] and abs(v['yaw']-90)<0.1 for v in values)
    checks[label+'_opening_has_intermediate_angles']=len({round(v['yaw'],1) for v in values if v['open'] and 1<v['yaw']<89})>=3
    checks[label+'_closing_has_intermediate_angles']=len({round(v['yaw'],1) for v in values if not v['open'] and 1<v['yaw']<89})>=3
    checks[label+'_closed_with_real_E']=not values[-1]['open'] and abs(values[-1]['yaw'])<0.1
ctx=unreal.load_asset('/Game/AIExample/Interaction/IMC_SurvivorInteraction')
mapping=ctx.get_editor_property('default_key_mappings').get_editor_property('mappings')[0]
checks['valid_E_binding']=mapping.get_editor_property('key').export_text()=='E'
result={'method':'Windows E keydown/keyup in focused client PIE viewport; no action injection','duration_seconds':0.6,'easing':'smoothstep ease-in/ease-out','checks':checks,'passed':all(checks.values()),'sample_count':len(keyboard_samples)}
folder=Path(unreal.Paths.project_saved_dir())/'InteractionValidation'
(folder/'keyboard-animation-result.json').write_text(json.dumps(result,indent=2))
(folder/'keyboard-animation-samples.json').write_text(json.dumps(keyboard_samples))
print(json.dumps(result))
