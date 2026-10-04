"""THROWAWAY owner acceptance of this probe's tiny, explicit contract only.

A Stop hook is evidence of a stopped response, not assignment completion.
This checks the native session, assignment identity and human-selected label.
It is not a durable delivery protocol, general validator, or exactly-once claim.
"""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
sessions = {'codex': '01a1040d-cd11-7470-b7bb-fee870c160f3',
            'claude': '136b9894-a43e-4907-8580-7e7e196e8875'}


def accept(event, provider):
    if event.get('hook_event_name') != 'Stop':
        return False
    if event.get('session_id') != sessions[provider]:
        return False
    try:
        result = json.loads(event.get('last_assistant_message', ''))
    except (ValueError, TypeError):
        return False
    return result == {'assignment_id': 'probe-recall-1',
                      'outcome': 'succeeded', 'label': 'pigscanfly'}


if __name__ == '__main__':
    for provider in sessions:
        path = root / (provider + '-hooks.jsonl')
        events = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
        # Do not reuse an older completed turn after a new dispatch. This
        # prototype serializes dispatches; production needs durable correlation.
        starts = [i for i, event in enumerate(events) if event.get('hook_event_name') == 'UserPromptSubmit']
        current = events[starts[-1]:] if starts else []
        stops = [event for event in current if event.get('hook_event_name') == 'Stop']
        candidate = stops[-1] if stops else {}
        interrupted = any(event.get('hook_event_name') == 'Interrupt' for event in current)
        correlated = bool(current) and (provider != 'codex' or candidate.get('turn_id') == current[0].get('turn_id'))
        print(json.dumps({'provider': provider, 'turn_ended': bool(stops),
                          'assignment_accepted': correlated and not interrupted and accept(candidate, provider)}))
