"""THROWAWAY launch of the two exact probe sessions with passive hooks."""
import json
import os
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
provider = sys.argv[1]
if provider == 'codex':
    command = ['codex', 'resume', '01a1040d-cd11-7470-b7bb-fee870c160f3',
               '--no-daemon', '--no-alt-screen', '-s', 'read-only', '-a', 'on-request']
    settings = json.loads((root / 'codex-hook-settings.json').read_text())
    for event, groups in settings['hooks'].items():
        hook_command = groups[0]['hooks'][0]['command']
        value = '[{ hooks = [{ type = "command", command = ' + json.dumps(hook_command) + ' }] }]'
        command += ['-c', 'hooks.' + event + '=' + value]
elif provider == 'claude':
    command = ['claude', '--resume', '136b9894-a43e-4907-8580-7e7e196e8875',
               '--permission-mode', 'manual', '--setting-sources', '',
               '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}',
               '--settings', str(root / 'claude-hook-settings.json')]
else:
    raise SystemExit('Expected codex or claude')
os.chdir(root)
os.execvp(command[0], command)
