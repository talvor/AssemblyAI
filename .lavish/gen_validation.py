"""Build the Lavish board for 'Choose validation and delivery ownership'.

usage: python3 gen_validation.py <questions.json> <answers.json> <round title> <intro> <out.html> [<figure.part.html>] [<facts.part.html>]
The answers file maps round -> {question id: answer}; it may be {}.
"""
import html
import json
import os
import sys

e = html.escape
qfile, afile, title, intro, out = sys.argv[1:6]
figure = open(sys.argv[6]).read() if len(sys.argv) > 6 and sys.argv[6] else ""
facts = open(sys.argv[7]).read() if len(sys.argv) > 7 and sys.argv[7] else ""
qs = json.load(open(qfile))
ans = json.load(open(afile)) if os.path.exists(afile) else {}

TICKET = "Choose validation and delivery ownership"
SETTLED_EARLIER = [
    ("Roles", "Engineering owns implementation; Quality owns independent review and validation, kept distinct from Engineering's responsibility. Workers do the substantive work, owning leaders accept results against the assignment's criteria, and a bare 'done' is never enough. Coordination owns unresolved cross-role trade-offs and cannot mark failed validation as passed.", "Define roles and leader-worker contracts", 5),
    ("Authority", "A tested-PR mandate covers checks, commits, pushing the job branch and opening or updating its PR. Merge, deployment and destructive changes outside the job need separate authorization unless a standing grant covers them. Accepting a tested PR does not authorize merging. A choice between distinct viable approaches is yours.", "Define delegated authority and human escalation", 6),
    ("Evidence", "Only evidence tied to the current dispatch counts. Workers record each push and each PR created or updated as an effect, and owning leaders reconcile effects against the real repository and GitHub state. The daemon-owned journal is the canonical record.", "Define work state and coordination contracts", 8),
    ("Branches", "Each job works in AsmAI's own clone. Writing assignments use their own assignment branches, pushed to origin. The job branch moves only when the daemon fast-forwards it to an accepted result, and only one party writes a branch at a time. The base is merged in unless the repository instructions ask for a rebase, and outside commits are kept and never force-pushed over. A notes-only job still delivers a PR. Agents use your git identity and credentials.", "Define concurrent repository work and integration", 11),
    ("Terminals and providers", "The daemon owns every agent terminal, with recordings, the input fence and worker caps (ADR 0001). Agents run AsmAI's pinned Claude Code and Codex, and AsmAI never writes ~/.claude or ~/.codex (ADR 0003).", "Define CLI setup and management experience", 9),
    ("Limits", "Worker caps of 3 per provider. An assignment that reaches 5 dispatches without acceptance holds and is escalated. Cancelling a job leaves its PR open. There are no notifications in v1.", "Define operating limits and visibility", 14),
    ("Skills", "Engineering workers carry implement, tdd and pr; Quality workers carry code-review, retro and tdd. A tested-PR mandate covers to-spec, to-tickets, implement and code-review. Where no-mistakes goes, and who opens the PR that the pr skill shapes, were left to this ticket.", "Choose skill bundles and update policy", 17),
]
settled_earlier = "".join(
    f'<li><b>{e(k)}:</b> {v} <span class="opacity-60">(<a class="link" href="https://github.com/talvor/AssemblyAI/issues/{n}">{e(name)}</a>)</span></li>'
    for k, v, name, n in SETTLED_EARLIER
)
settled_here = "".join(f"<li><b>{e(k)}</b>: {e(v)}</li>" for r in ans.values() for k, v in r.items())

cards = []
for q in qs:
    i = q["id"]
    opts = "".join(
        f'<label class="choice"><input type="radio" class="radio radio-primary" name="answer" value="{e(o)}"><span>{e(o)}</span></label>'
        for o in q["options"]
    )
    extra = ""
    if q.get("points"):
        extra = '<ol class="list-decimal ml-6 mb-4 space-y-2 opacity-95">' + "".join(f"<li>{e(x)}</li>" for x in q["points"]) + "</ol>"
    if not q["options"]:
        cards.append(
            f'''<section class="card bg-base-200 p-6 mb-5"><p class="text-success text-sm font-bold mb-1">{i}</p><h2 class="text-xl font-bold mb-3">{e(q['title'])}</h2><p class="mb-3 opacity-90">{e(q['body'])}</p>{extra}</section>'''
        )
        continue
    cards.append(
        f'''<form class="card bg-base-200 p-6 mb-5" data-lavish-question="{i}" onsubmit="event.preventDefault();const f=new FormData(this);const a=f.get('answer');const n=(f.get('notes')||'').trim();if(!a&&!n)return;if(window.lavish)window.lavish.queuePrompt('{i} answer: '+(a||'(no option)')+(n?' | Notes: '+n:''),{{tag:'choice',text:'{i}: '+(a||n),element:this,data:{{question:'{i}',answer:a,notes:n}}}});this.querySelector('.queued').textContent=window.lavish?'Queued ✓':'Open this page in Lavish to send answers';">
<p class="text-primary text-sm font-bold mb-1">{i}</p><h2 class="text-xl font-bold mb-3">{e(q['title'])}</h2>
<p class="mb-3 opacity-90">{e(q['body'])}</p>
{extra}
{f'<div class="rec mb-4"><span class="font-bold">Recommended:</span> {e(q["rec"])}</div>' if q.get('rec') else ''}
<div class="grid gap-2 mb-3">{opts}</div>
<textarea name="notes" class="textarea w-full mb-3" rows="2" placeholder="Notes, conditions, or a different answer"></textarea>
<div class="flex items-center gap-3"><button class="btn btn-primary btn-sm" type="submit">Queue answer</button><span class="queued text-success text-sm"></span></div></form>'''
    )

settled_block = (
    f'<details class="card bg-base-300 p-5 mb-6"><summary class="font-bold cursor-pointer">Settled in this ticket so far</summary><ul class="list-disc ml-6 mt-3 opacity-90">{settled_here}</ul></details>'
    if settled_here
    else ""
)

has_forms = any(q["options"] for q in qs)
QHEAD = ('<h2 class="text-2xl font-bold mb-2">Questions</h2><p class="opacity-80 mb-5">Queue an answer for each question, add notes where you want, then press <b>Send to Agent</b>.</p>' if has_forms else '<h2 class="text-2xl font-bold mb-4">Resolution</h2>')
QFOOT = ('<p class="opacity-70">Queue an answer for each question, then press <b>Send to Agent</b>.</p>' if has_forms else '')
page = f'''<!doctype html>
<html lang="en" data-theme="night">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AsmAI · Validation and delivery</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/daisyui.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/themes.css">
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.2.4/dist/index.global.js"></script>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#0f1729;color:#e2e8f0;font-family:system-ui,sans-serif}}main{{max-width:900px;margin:auto;padding:40px 24px}}p,h1,h2,label,span,li{{overflow-wrap:anywhere}}.card{{min-width:0}}label.choice{{display:flex;align-items:center;gap:12px;padding:12px 14px;border:1px solid #334155;border-radius:10px;cursor:pointer}}label.choice:has(:checked){{border-color:#38bdf8;background:#132e43}}textarea{{max-width:100%}}.rec{{border-left:3px solid #38bdf8;padding:8px 12px;background:#0b2233;border-radius:6px}}code{{font-size:.88em;color:#bae6fd}}.flow{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:10px}}.flow li{{flex:1 1 150px;min-width:0;border-radius:10px;padding:10px 12px;position:relative}}.flow li b{{display:block;margin-bottom:2px}}.flow li span{{font-size:.85em;opacity:.85}}.flow li.settled{{background:#0f2e22;border:1px solid #22c55e}}.flow li.open{{background:#33260b;border:1px solid #f59e0b}}</style></head>
<body>
<main><header class="mb-6"><p class="text-primary text-sm tracking-widest uppercase mb-3">AsmAI / Wayfinder / {e(TICKET)}</p>
<h1 class="text-4xl font-bold mb-4">{e(title)}</h1><p class="text-lg opacity-80">{e(intro)}</p></header>
<details class="card bg-base-300 p-5 mb-6"><summary class="font-bold cursor-pointer">Settled by earlier tickets (this round builds on these)</summary><ul class="list-disc ml-6 mt-3 opacity-90 space-y-2">{settled_earlier}</ul></details>
{settled_block}
{facts}
{figure}
{QHEAD}
{"".join(cards)}
{QFOOT}
</main></body></html>'''
open(out, "w").write(page)
print(out)
