"""Render acceptance-cases.json as the board's table of cases deferred here by earlier tickets."""
import html, json, re, sys

NAMES = {
    7: "Choose factory hosting and lifecycle",
    8: "Define work state and coordination contracts",
    9: "Define CLI setup and management experience",
    10: "Explore terminal conversation and Lavish decision flow",
    11: "Define concurrent repository work and integration",
    14: "Define operating limits and visibility",
    15: "Choose runtime adapters and authentication",
    17: "Choose skill bundles and update policy",
    18: "Choose validation and delivery ownership",
    19: "Validate interactive CLI coordination and intervention",
}

def inline(t):
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(t, quote=False))

groups = json.load(open(sys.argv[1]))
total = sum(len(g["cases"]) for g in groups)
rows = []
for g in groups:
    rows.append(f'<tr class="grp"><td colspan="3">{html.escape(g["group"])}</td></tr>')
    for cid, text, src in g["cases"]:
        links = "<br>".join(f'<a class="link" href="https://github.com/talvor/AssemblyAI/issues/{n}">{html.escape(NAMES[n])}</a>' for n in src)
        rows.append(f'<tr><td class="id">{cid}</td><td>{inline(text)}</td><td class="text-xs opacity-80">{links}</td></tr>')
print(f'''<details class="card bg-base-300 p-5 mb-6" open><summary class="font-bold cursor-pointer text-xl">The {total} cases earlier tickets left here to qualify</summary>
<p class="text-sm opacity-70 mt-2 mb-3">Gathered from the resolution comments of nine closed tickets. Each was deferred because an earlier decision relies on it being true, and none has been demonstrated beyond the local feasibility probes. Q6 asks whether this is the v1 qualification list.</p>
<div class="overflow-x-auto"><table class="table table-sm cases"><thead><tr><th>Case</th><th>What must be shown</th><th>Deferred by</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></details>''')
