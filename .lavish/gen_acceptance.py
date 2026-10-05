"""Build the Lavish board for 'Define v1 acceptance scenarios and evidence'.

usage: python3 gen_acceptance.py <questions.json> <answers.json> <round title> <intro> <out.html> [<part.html> ...]
The answers file maps round -> {question title: answer}; it may be {}.
Part files are inserted, in order, between the settled sections and the questions.
"""
import html
import json
import os
import sys

e = html.escape
qfile, afile, title, intro, out = sys.argv[1:6]
parts = "".join(open(p).read() for p in sys.argv[6:] if p)
qs = json.load(open(qfile))
ans = json.load(open(afile)) if os.path.exists(afile) else {}

TICKET = "Define v1 acceptance scenarios and evidence"
SETTLED_EARLIER = [
    ("Tested PR", "A tested pull request's exact head has passed Quality's validation and the repository's CI, with its base taken in and its evidence and gaps stated in the PR. AsmAI never merges it, and the job ends when it is delivered. This ticket keeps the proving-ground task, the scenarios that show a tested PR being delivered, and qualifying the delivery mechanics.", "Choose validation and delivery ownership", 18),
    ("Qualification and platforms", "AsmAI supports only qualified combinations of its pinned providers and refuses others before any dispatch. Linux and macOS are both v1 platforms, held to one bar and certified per platform; Linux may launch before macOS. v1 recovers with work intact from a terminal or SSH disconnect, an agent crash, a daemon crash and a host reboot.", "Choose factory hosting and lifecycle", 7),
    ("Providers", "Both Claude and Codex are launch requirements, with mixed staffing. Each user signs in to the unmodified provider CLIs themselves; AsmAI never starts a login, handles tokens or uses API billing. Codex 0.157.0 and Claude Code 2.1.283 are candidate baselines, not certified versions.", "Choose runtime adapters and authentication", 15),
    ("Adapter contract", "Unmodified interactive CLIs with passive hooks. Missing, conflicting or stale signals mean unknown and need reconciliation; nothing is inferred from silence, screen text or process exit. The local probes proved feasibility only, not launch support.", "Validate interactive CLI coordination and intervention", 19),
    ("Work state", "Only evidence tied to the current dispatch counts. Effects are recorded as they happen, and owning leaders reconcile them against real state, with no blind retries. The daemon's journal is the canonical record, and `asmai export` exports it.", "Define work state and coordination contracts", 8),
    ("Human decisions", "You choose between distinct viable approaches. Single choices are answered in the conversation and the rest in Lavish, one answer surface per version, and only witnessed messages count as your words. Independent work continues while a decision is pending.", "Explore terminal conversation and Lavish decision flow", 10),
    ("Limits", "Worker caps of 3 per provider; holds when allowance runs out, a provider fails or sign-in is lost, resuming when the cause clears; no spending without a grant; `asmai job pause|resume|cancel`; terminal recordings per dispatch.", "Define operating limits and visibility", 14),
    ("Repositories", "Each job works in AsmAI's own clone, never your checkout. A repository can be declared as having no CI. Concurrent jobs in one repository run with no locks.", "Define concurrent repository work and integration", 11),
]
settled_earlier = "".join(
    f'<li><b>{e(k)}:</b> {e(v)} <span class="opacity-60">(<a class="link" href="https://github.com/talvor/AssemblyAI/issues/{n}">{e(name)}</a>)</span></li>'
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
    body = "".join(f'<p class="mb-3 opacity-90">{e(p)}</p>' for p in q["body"].split("\n\n"))
    if not q["options"]:
        cards.append(
            f'''<section class="card bg-base-200 p-6 mb-5"><p class="text-success text-sm font-bold mb-1">{i}</p><h2 class="text-xl font-bold mb-3">{e(q['title'])}</h2>{body}{extra}</section>'''
        )
        continue
    cards.append(
        f'''<form class="card bg-base-200 p-6 mb-5" data-lavish-question="{i}" onsubmit="event.preventDefault();const f=new FormData(this);const a=f.get('answer');const n=(f.get('notes')||'').trim();if(!a&&!n)return;if(window.lavish)window.lavish.queuePrompt('{i} answer: '+(a||'(no option)')+(n?' | Notes: '+n:''),{{tag:'choice',text:'{i}: '+(a||n),element:this,data:{{question:'{i}',answer:a,notes:n}}}});this.querySelector('.queued').textContent=window.lavish?'Queued ✓':'Open this page in Lavish to send answers';">
<p class="text-primary text-sm font-bold mb-1">{i}</p><h2 class="text-xl font-bold mb-3">{e(q['title'])}</h2>
{body}
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
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AsmAI · Acceptance and qualification</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/daisyui.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/themes.css">
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.2.4/dist/index.global.js"></script>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#0f1729;color:#e2e8f0;font-family:system-ui,sans-serif}}main{{max-width:900px;margin:auto;padding:40px 24px}}p,h1,h2,label,span,li,td{{overflow-wrap:anywhere}}.card{{min-width:0}}label.choice{{display:flex;align-items:center;gap:12px;padding:12px 14px;border:1px solid #334155;border-radius:10px;cursor:pointer}}label.choice:has(:checked){{border-color:#38bdf8;background:#132e43}}textarea{{max-width:100%}}.rec{{border-left:3px solid #38bdf8;padding:8px 12px;background:#0b2233;border-radius:6px}}code{{font-size:.88em;color:#bae6fd}}.flow{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:10px}}.flow li{{flex:1 1 150px;min-width:0;border-radius:10px;padding:10px 12px;position:relative}}.flow li b{{display:block;margin-bottom:2px}}.flow li span{{font-size:.85em;opacity:.85}}.flow li.settled{{background:#0f2e22;border:1px solid #22c55e}}.flow li.open{{background:#33260b;border:1px solid #f59e0b}}table.cases td,table.cases th{{vertical-align:top}}table.cases td.id{{white-space:nowrap;color:#7dd3fc;font-weight:600}}table.cases tr.grp td{{background:#1e293b;font-weight:700;color:#fbbf24}}</style></head>
<body>
<main><header class="mb-6"><p class="text-primary text-sm tracking-widest uppercase mb-3">AsmAI / Wayfinder / {e(TICKET)}</p>
<h1 class="text-4xl font-bold mb-4">{e(title)}</h1><p class="text-lg opacity-80">{e(intro)}</p></header>
<details class="card bg-base-300 p-5 mb-6"><summary class="font-bold cursor-pointer">Settled by earlier tickets (this round builds on these)</summary><ul class="list-disc ml-6 mt-3 opacity-90 space-y-2">{settled_earlier}</ul></details>
{settled_block}
{parts}
{QHEAD}
{"".join(cards)}
{QFOOT}
</main></body></html>'''
open(out, "w").write(page)
print(out)
