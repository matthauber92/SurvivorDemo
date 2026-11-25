"""Run a project script in the local SurvivorDemo editor via Epic's Python API."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, r'C:\Users\Matt Hauber\Epic Games\UE_5.8\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python')
import remote_execution

remote = remote_execution.RemoteExecution()
remote.start()
try:
    for _ in range(20):
        nodes = [n for n in remote.remote_nodes if n.get('project_name') == 'SurvivorDemo']
        if nodes:
            break
        time.sleep(0.5)
    if len(nodes) != 1:
        raise RuntimeError('Expected one SurvivorDemo editor: ' + json.dumps(remote.remote_nodes))
    remote.open_command_connection(nodes[0]['node_id'])
    script = Path(sys.argv[1]).resolve()
    response = remote.run_command(str(script), unattended=True)
    print(json.dumps(response, indent=2))
    if not response.get('success'):
        sys.exit(1)
finally:
    remote.stop()
