"""Build the Lavish review board for one document of the AsmAI v1 specification.

usage: python3 gen_spec_doc.py <board.json>

board.json holds:
  doc        path of the Markdown document under review
  name       the document's name, for example "00 Overview"
  round      round label, for example "Round 1"
  intro      one paragraph shown under the title
  questions  path of the questions JSON: [{id, title, body, rec, options, section?}]
  answers    path of the recorded answers JSON (may be missing): {round: {question: answer}}
  notes      list of drafting notes: things decided by drafting, open to annotation
  changes    list of changes made since the last round (optional)
  out        path of the HTML board to write
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spec_md import render, slug  # noqa: E402

e = html.escape
cfg = json.load(open(sys.argv[1]))
qs = json.load(open(cfg["questions"]))
ans = json.load(open(cfg["answers"])) if cfg.get("answers") and os.path.exists(cfg["answers"]) else {}
doc_html = render(open(cfg["doc"]).read())

answered = "".join(
    f"<li><b>{e(k)}</b>: {e(v)}</li>" for r in ans.values() for k, v in r.items()
)
answered_block = (
    f'<details class="card bg-base-300 p-5 mb-6"><summary class="font-bold cursor-pointer">Answered in earlier rounds</summary><ul class="list-disc ml-6 mt-3 space-y-1 opacity-90">{answered}</ul></details>'
    if answered
    else ""
)
changes = cfg.get("changes") or []
changes_block = (
    '<section class="card bg-base-300 p-5 mb-6"><h2 class="text-xl font-bold mb-2">Changed since the last round</h2><ul class="list-disc ml-6 space-y-1">'
    + "".join(f"<li>{e(c)}</li>" for c in changes)
    + "</ul></section>"
    if changes
    else ""
)
notes = cfg.get("notes") or []
notes_block = (
    '<section class="card bg-base-300 p-5 mb-6"><h2 class="text-xl font-bold mb-2">Drafting notes</h2><p class="opacity-80 mb-2">Choices of arrangement the sources leave to the drafting, not decisions. Annotate any you want changed.</p><ul class="list-disc ml-6 space-y-2">'
    + "".join(f"<li>{e(n)}</li>" for n in notes)
    + "</ul></section>"
    if notes
    else ""
)

cards = []
for q in qs:
    i = q["id"]
    body = "".join(f'<p class="mb-3 opacity-90">{e(p)}</p>' for p in q["body"].split("\n\n"))
    where = (
        f'<p class="text-sm mb-3"><a class="link" href="#{e(slug(q["section"]))}">Go to “{e(q["section"])}” in the document</a></p>'
        if q.get("section")
        else ""
    )
    opts = "".join(
        f'<label class="choice"><input type="radio" class="radio radio-primary" name="answer" value="{e(o)}"><span>{e(o)}</span></label>'
        for o in q["options"]
    )
    rec = f'<div class="rec mb-4"><span class="font-bold">Recommended:</span> {e(q["rec"])}</div>' if q.get("rec") else ""
    cards.append(
        f'''<form class="card bg-base-200 p-6 mb-5" data-lavish-question="{e(i)}" onsubmit="event.preventDefault();const f=new FormData(this);const a=f.get('answer');const n=(f.get('notes')||'').trim();if(!a&&!n)return;if(window.lavish)window.lavish.queuePrompt('{e(i)} answer: '+(a||'(no option)')+(n?' | Notes: '+n:''),{{tag:'choice',text:'{e(i)}: '+(a||n),element:this,data:{{question:'{e(i)}',answer:a,notes:n}}}});this.querySelector('.queued').textContent=window.lavish?'Queued ✓':'Open this page in Lavish to send answers';">
<p class="text-primary text-sm font-bold mb-1">{e(i)}</p><h3 class="text-xl font-bold mb-3">{e(q["title"])}</h3>
{where}{body}{rec}
<div class="grid gap-2 mb-3">{opts}</div>
<textarea name="notes" class="textarea w-full mb-3" rows="2" placeholder="Notes, conditions, or a different answer"></textarea>
<div class="flex items-center gap-3"><button class="btn btn-primary btn-sm" type="submit">Queue answer</button><span class="queued text-success text-sm"></span></div></form>'''
    )

page = f"""<!doctype html>
<html lang="en" data-theme="night">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AsmAI spec · {e(cfg["name"])}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/daisyui.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/themes.css">
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.2.4/dist/index.global.js"></script>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#0f1729;color:#e2e8f0;font-family:system-ui,sans-serif}}main{{max-width:1040px;margin:auto;padding:40px 24px}}p,h1,h2,h3,label,span,li,td,th{{overflow-wrap:anywhere}}.card{{min-width:0}}label.choice{{display:flex;align-items:center;gap:12px;padding:12px 14px;border:1px solid #334155;border-radius:10px;cursor:pointer}}label.choice:has(:checked){{border-color:#38bdf8;background:#132e43}}textarea{{max-width:100%}}.rec{{border-left:3px solid #38bdf8;padding:8px 12px;background:#0b2233;border-radius:6px}}code{{font-size:.88em;color:#bae6fd}}.doc{{background:#111c33;border:1px solid #1e3a5f;border-radius:14px;padding:28px}}.doc table td,.doc table th{{vertical-align:top}}.doc a.link{{color:#7dd3fc}}.quote{{border-left:3px solid #64748b;padding:6px 12px;opacity:.9}}</style></head>
<body><main>
<header class="mb-6"><p class="text-primary text-sm tracking-widest uppercase mb-3">AsmAI / v1 specification / review</p>
<h1 class="text-4xl font-bold mb-3">{e(cfg["name"])} · {e(cfg["round"])}</h1>
<p class="text-lg opacity-80">{e(cfg["intro"])}</p></header>
{answered_block}
{changes_block}
<h2 class="text-2xl font-bold mb-2">Questions</h2>
<p class="opacity-80 mb-5">Queue an answer for each question, annotate anything in the document you want changed, then press <b>Send to Agent</b>.</p>
{"".join(cards)}
{notes_block}
<h2 class="text-2xl font-bold mb-3">The document</h2>
<p class="opacity-70 mb-3"><code>{e(cfg["doc"])}</code> as drafted. Links point at talvor/AssemblyAI; links to other specification documents work once they are merged.</p>
<article class="doc mb-8" id="document">{doc_html}</article>
<p class="opacity-70">Queue your answers and annotations, then press <b>Send to Agent</b>.</p>
</main></body></html>"""
open(cfg["out"], "w").write(page)
print(cfg["out"])
