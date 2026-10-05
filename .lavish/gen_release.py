"""Build the Lavish board for 'Choose license, release packaging and upgrade migration'.

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

TICKET = "Choose license, release packaging and upgrade migration"
SETTLED_EARLIER = [
    ("Open source", "AsmAI v1 is open-source and user-operated, including on your own remote hosts. A hosted service, commercial distribution and resale of provider access are outside AsmAI's own v1 direction. The license was left to this ticket.", "Choose runtime adapters and authentication", 15),
    ("Reuse", "Copying a component from Firstmate or OpenRig needs a separate decision that reviews its license and notice requirements. Ordinary third-party libraries are not restricted.", "Choose inspiration versus reuse of reference systems", 16),
    ("Names and channels", "<code>asmai</code> is the name on every channel; <code>assemblyai</code> is never an identifier. One self-contained Go executable with SQLite built in, published on GitHub Releases with checksums, through a Homebrew tap, and by an install script into <code>~/.local/bin</code>, with no root. The names are to be claimed when implementation starts. Config is <code>~/.config/asmai/config.toml</code>; state is <code>~/.local/state/asmai</code>; <code>asmai backup &lt;file&gt;</code> takes a consistent copy of the store while the factory runs.", "Define CLI setup and management experience", 9),
    ("Upgrades", "Through the install channel: stop, upgrade, start. No hot upgrade and no self-update; <code>asmai doctor</code> reports newer releases. The daemon checks provider versions at start and refuses unqualified combinations. Agents run AsmAI's own pinned Claude Code, Codex and Lavish, installed with <code>asmai providers install</code> from official channels (ADR 0003).", "Choose factory hosting and lifecycle", 7),
    ("Store", "The daemon is the only writer of an embedded SQLite store; its append-only journal is kept in full. The user is responsible for backing up the state directory; losing the host or moving the factory is out of v1.", "Define work state and coordination contracts", 8),
    ("Skills", "Each release embeds one pinned upstream skill release, with its MIT notice, inside the executable; releases carry that notice. After an upgrade, work continues on the new bundle from the next dispatch.", "Choose skill bundles and update policy", 17),
    ("Qualification", "A platform is an operating system and CPU architecture, Linux x86_64 first. Before each release the maintainer qualifies every certified platform on a real host with the real pinned providers. The release carries a qualification record (qualified combinations, certified platforms, known limitations); <code>asmai start</code> refuses anything else. No qualification runs in hosted CI and there is no <code>asmai qualify</code> command. v1 launches when Linux is certified and the proving scenarios pass; macOS follows. Case C5: Codex hook trust survives an AsmAI upgrade.", "Define v1 acceptance scenarios and evidence", 12),
    ("Disk", "Below 5 GB free on the state directory's volume no new workspace is created; <code>asmai status</code> reports disk use, including the store.", "Define operating limits and visibility", 14),
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
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AsmAI · License, releases and upgrades</title>
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
