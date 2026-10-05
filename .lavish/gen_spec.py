"""Build the Lavish board for 'Choose the specification's structure and implementation sequence'.

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

TICKET = "Choose the specification's structure and implementation sequence"
SETTLED_EARLIER = [
    ("Destination", "An implementation-ready v1 specification for AsmAI, settling enough decisions that implementation can begin without unresolved foundational choices. The map is planning only and authorizes no implementation.", "Chart AsmAI", 1),
    ("Launch", "v1 launches on Linux after two gates: all 47 qualification cases pass with the real pinned providers on each certified platform, and nine proving scenarios on real repositories, headed by AsmAI's v2 notify command delivered as a tested PR (S1), each pass their evidence checklist and your verdict. The remote scenario runs on a virtual machine you set up when it is needed.", "Define v1 acceptance scenarios and evidence", 12),
    ("Qualification", "A harness drives the release's pinned Claude Code, Codex and Lavish on a real host, under a separate OS user with its own sign-in and its own factory, with faults injected. Simulated providers never qualify, nothing runs in hosted CI, and delivery cases use a GitHub fixture repository you own (ADR 0008).", "Define v1 acceptance scenarios and evidence", 12),
    ("Releases", "Apache-2.0. A release is the qualified commit plus its qualification record, built and attested in GitHub Actions for certified platforms only (Linux x86_64 first, macOS on Apple silicon later), from the repository renamed talvor/asmai before the first release. Release candidates are prereleases used for the proving scenarios. The install script is the only channel. The store migrates forward-only, and every release keeps all migrations since v1.0. Renaming the repository and building the release workflow were left for this ticket to order.", "Choose license, release packaging and upgrade migration", 20),
    ("Configuration", "One TOML file at ~/.config/asmai/config.toml, edited by commands and applied with asmai config apply, and never rewritten by an upgrade. What its settings mean and their defaults are settled across six tickets; field names and agent instructions are still fog on the map.", "Define CLI setup and management experience", 9),
    ("Delivery", "Engineering tests its own work; Quality validates the finished job branch at its exact head; the daemon pushes and watches CI; the Engineering leader opens the PR; AsmAI never merges (ADR 0007).", "Choose validation and delivery ownership", 18),
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
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AsmAI · Specification and sequence</title>
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
