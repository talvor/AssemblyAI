"""Build the Lavish board for 'Choose skill bundles and update policy'.

usage: python3 gen_skills.py <questions.json> <answers.json> <round title> <intro> <out.html> [<figure.part.html>] [<facts.part.html>]
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

TICKET = "Choose skill bundles and update policy"
SETTLED_EARLIER = [
    ("Skill inventory", "37 Matt Pocock skills verified against upstream, plus lavish, no-mistakes and find-skills, which are separate integrations. Six upstream skills are in progress. Role groupings there were proposals only.", "Map Matt Pocock skills to factory roles", 3),
    ("Roles", "Coordination, Planning, Research, Engineering and Quality, each with one leader; workers do substantive research, implementation, prototypes and independent validation. Skills are reusable methods, not exclusive permissions.", "Define roles and leader-worker contracts", 5),
    ("Authority", "Approvals are recorded with their scope and conditions and reused while they hold; a job approval stays with its job; wider reuse needs an explicit grant. Human grilling and Wayfinder need your actual answer. A choice between distinct viable approaches is yours.", "Define delegated authority and human escalation", 6),
    ("Providers", "Both Claude and Codex at launch, mixed staffing, and only explicitly tested version combinations are supported.", "Choose runtime adapters and authentication", 15),
    ("Setup and configuration", "Agents run AsmAI's own pinned Claude Code, Codex and Lavish. Settings, role instructions and skills are passed per session (Claude <code>--plugin-dir</code> and <code>--setting-sources</code>, Codex <code>-c</code>); AsmAI never writes <code>~/.claude</code> or <code>~/.codex</code>. Each role has a leader skill list and a worker skill list, and an assignment may narrow the worker list. Skill contents, versions, overrides, hiding personal skills and delivering skills to Codex were left to this ticket.", "Define CLI setup and management experience", 9),
    ("Decision requests", "Grilling and Wayfinder questions are emitted as structured decision requests that the daemon renders; single choices are answered in the conversation and the rest in Lavish.", "Explore terminal conversation and Lavish decision flow", 10),
    ("Repositories", "Each job works in AsmAI's own clone; the daemon creates workspaces. A repository's instruction files apply; its provider configuration (.claude, .codex) does not. Skills a repository provides were left to this ticket.", "Define concurrent repository work and integration", 11),
    ("Still open", "Whether no-mistakes is adopted, and who drives it, is decided in a separate ticket.", "Choose validation and delivery ownership", 18),
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
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AsmAI · Skill bundles</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/daisyui.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/themes.css">
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.2.4/dist/index.global.js"></script>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#0f1729;color:#e2e8f0;font-family:system-ui,sans-serif}}main{{max-width:900px;margin:auto;padding:40px 24px}}p,h1,h2,label,span,li{{overflow-wrap:anywhere}}.card{{min-width:0}}label.choice{{display:flex;align-items:center;gap:12px;padding:12px 14px;border:1px solid #334155;border-radius:10px;cursor:pointer}}label.choice:has(:checked){{border-color:#38bdf8;background:#132e43}}textarea{{max-width:100%}}.rec{{border-left:3px solid #38bdf8;padding:8px 12px;background:#0b2233;border-radius:6px}}code{{font-size:.88em;color:#bae6fd}}</style></head>
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
