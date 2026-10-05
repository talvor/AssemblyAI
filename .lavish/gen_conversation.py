"""Build the Lavish board for 'Explore terminal conversation and Lavish decision flow'.

usage: python3 gen_conversation.py <questions.json> <answers.json> <round title> <intro> <out.html>
The answers file maps round -> {question id: answer}; it may be {}.
"""
import html
import json
import os
import sys

e = html.escape
here = os.path.dirname(os.path.abspath(__file__))
qfile, afile, title, intro, out = sys.argv[1:6]
qs = json.load(open(qfile))
ans = json.load(open(afile)) if os.path.exists(afile) else {}
proto = open(os.path.join(here, "conversation-prototype.part.html")).read()

TICKET = "Explore terminal conversation and Lavish decision flow"
SETTLED_EARLIER = [
    ("Conversation", "Coordination's provider screen (Claude Code or Codex) is the conversation, and bare <code>asmai</code> opens it. It is not an intervention: detaching returns Coordination to automated delivery, and the daemon never types into it while you have unsent text.", "Define CLI setup and management experience", 9),
    ("Delivery", "The daemon types only a one-line nudge carrying a dispatch ID, at an input-ready boundary. The agent's <code>asmai inbox</code> fetch is the delivery evidence; content never travels through the terminal.", "Define work state and coordination contracts", 8),
    ("Lavish", "Required for reviews and for all grilling and Wayfinder questions. The daemon supervises the Lavish server on localhost; remote hosts use SSH forwarding, and <code>asmai lavish</code> lists pending pages.", "Choose factory hosting and lifecycle", 7),
    ("Decisions", "Versioned: a stale reply cannot approve a changed request. Escalate once and update when material new evidence arrives. Dependent work pauses and independent work continues.", "Define delegated authority and human escalation", 6),
    ("Intervention", "Attaching observes; taking input is explicit and waits for a boundary (or <code>--interrupt</code>); automated drafts are recorded and cleared; native prompts are a boundary and are answered in place; release is explicit, and detaching without releasing keeps automation paused. A Ctrl-] menu offers detach, take, release and interrupt.", "Choose factory hosting and lifecycle", 7),
    ("Roles", "Coordination is your single counterpart and carries each exchange faithfully; the owning leader owns the substance; agents never supply your side.", "Define roles and leader-worker contracts", 5),
    ("Elsewhere", "Notifications while you are away, and what job cancel, pause and resume do, belong to Define operating limits and visibility. A separate browser dashboard is not assumed.", "Define operating limits and visibility", 14),
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
    tryline = f'<p class="try mb-3"><b>In the prototype:</b> {e(q["try"])}</p>' if q.get("try") else ""
    if q.get("points"):
        tryline += '<ol class="list-decimal ml-6 mb-4 space-y-2 opacity-95">' + "".join(f"<li>{e(x)}</li>" for x in q["points"]) + "</ol>"
    cards.append(
        f'''<form class="card bg-base-200 p-6 mb-5" data-lavish-question="{i}" onsubmit="event.preventDefault();const f=new FormData(this);const a=f.get('answer');const n=(f.get('notes')||'').trim();if(!a&&!n)return;if(window.lavish)window.lavish.queuePrompt('{i} answer: '+(a||'(no option)')+(n?' | Notes: '+n:''),{{tag:'choice',text:'{i}: '+(a||n),element:this,data:{{question:'{i}',answer:a,notes:n}}}});this.querySelector('.queued').textContent=window.lavish?'Queued ✓':'Open this page in Lavish to send answers';">
<p class="text-primary text-sm font-bold mb-1">{i}</p><h2 class="text-xl font-bold mb-3">{e(q['title'])}</h2>
<p class="mb-3 opacity-90">{e(q['body'])}</p>
{tryline}
{f'<div class="rec mb-4"><span class="font-bold">Recommended:</span> {e(q["rec"])}</div>' if q.get('rec') else ''}
<div class="grid gap-2 mb-3">{opts}</div>
<textarea name="notes" class="textarea w-full mb-3" rows="2" placeholder="Notes, conditions, or a different answer"></textarea>
<div class="flex items-center gap-3"><button class="btn btn-primary btn-sm" type="submit">Queue answer</button><span class="queued text-success text-sm"></span></div></form>'''
    )
    if not q["options"]:
        cards[-1] = f'''<section class="card bg-base-200 p-6 mb-5"><p class="text-success text-sm font-bold mb-1">{i}</p><h2 class="text-xl font-bold mb-3">{e(q['title'])}</h2><p class="mb-3 opacity-90">{e(q['body'])}</p>{tryline}</section>'''

settled_block = (
    f'<details class="card bg-base-300 p-5 mb-6"><summary class="font-bold cursor-pointer">Settled in this ticket so far</summary><ul class="list-disc ml-6 mt-3 opacity-90">{settled_here}</ul></details>'
    if settled_here
    else ""
)

has_forms = any(q["options"] for q in qs)
QHEAD = ('<h2 class="text-2xl font-bold mb-2">Questions</h2><p class="opacity-80 mb-5">Each question names the prototype setting and scenario that shows it. Queue an answer for each, add notes where you want, then press <b>Send to Agent</b>.</p>' if has_forms else '<h2 class="text-2xl font-bold mb-4">Resolution</h2>')
QFOOT = ('<p class="opacity-70">Queue an answer for each question, then press <b>Send to Agent</b>.</p>' if has_forms else '')
page = f'''<!doctype html>
<html lang="en" data-theme="night">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AsmAI · Conversation and Lavish flow</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/daisyui.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/themes.css">
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.2.4/dist/index.global.js"></script>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#0f1729;color:#e2e8f0;font-family:system-ui,sans-serif}}main{{max-width:900px;margin:auto;padding:40px 24px}}p,h1,h2,label,span,li{{overflow-wrap:anywhere}}.card{{min-width:0}}label.choice{{display:flex;align-items:center;gap:12px;padding:12px 14px;border:1px solid #334155;border-radius:10px;cursor:pointer}}label.choice:has(:checked){{border-color:#38bdf8;background:#132e43}}textarea{{max-width:100%}}.rec{{border-left:3px solid #38bdf8;padding:8px 12px;background:#0b2233;border-radius:6px}}.try{{border-left:3px solid #fbbf24;padding:6px 12px;background:#2a2210;border-radius:6px;font-size:.92rem}}code{{font-size:.88em;color:#bae6fd}}</style></head>
<body>
<main class="pb-0"><header class="mb-6"><p class="text-primary text-sm tracking-widest uppercase mb-3">AsmAI / Wayfinder / {e(TICKET)}</p>
<h1 class="text-4xl font-bold mb-4">{e(title)}</h1><p class="text-lg opacity-80">{e(intro)}</p></header>
<details class="card bg-base-300 p-5 mb-6"><summary class="font-bold cursor-pointer">Settled by earlier tickets (this round builds on these)</summary><ul class="list-disc ml-6 mt-3 opacity-90 space-y-2">{settled_earlier}</ul></details>
{settled_block}
</main>
{proto}
<main class="pt-0">
{QHEAD}
{"".join(cards)}
{QFOOT}
</main></body></html>'''
open(out, "w").write(page)
print(out)
