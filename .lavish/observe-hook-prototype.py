"""THROWAWAY passive lifecycle recorder. Never approves, denies or continues."""
import json
import sys
import time
from pathlib import Path

payload = json.load(sys.stdin)
fields = ['hook_event_name', 'session_id', 'turn_id', 'permission_mode',
          'tool_name', 'stop_hook_active', 'last_assistant_message', 'error']
record = {key: payload[key] for key in fields if key in payload}
record['observed_at'] = time.time()
record['source'] = sys.argv[1]
with Path(__file__).with_name(sys.argv[1] + '-hooks.jsonl').open('a') as output:
    output.write(json.dumps(record) + '\n')
print('{}')
