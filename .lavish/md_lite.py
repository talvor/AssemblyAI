"""Render the small Markdown subset used in resolution files to HTML: headings, nested bullets, tables, paragraphs, code, bold, links."""
import html, re, sys

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a class="link" href="\2">\1</a>', t)
    return t

def render(md):
    out, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1; continue
        m = re.match(r"(#{2,4}) (.*)", l)
        if m:
            sz = {2: "text-2xl", 3: "text-xl", 4: "text-lg"}[len(m.group(1))]
            out.append(f'<h{len(m.group(1))} class="{sz} font-bold mt-5 mb-2">{inline(m.group(2))}</h{len(m.group(1))}>'); i += 1; continue
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"-+", c) for c in cells): rows.append(cells)
                i += 1
            head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            body = "".join("<tr>" + "".join(f'<td class="align-top">{inline(c)}</td>' for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="overflow-x-auto"><table class="table table-sm"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'); continue
        if re.match(r"\s*- ", l):
            html_list, depth = [], -1
            while i < len(lines) and (re.match(r"\s*- ", lines[i]) or (lines[i].startswith("  ") and lines[i].strip())):
                if not re.match(r"\s*- ", lines[i]):
                    html_list.append("<p>" + inline(lines[i].strip()) + "</p>"); i += 1; continue
                d = (len(lines[i]) - len(lines[i].lstrip())) // 2
                while depth < d:
                    html_list.append('<ul class="list-disc ml-6 space-y-1">'); depth += 1
                while depth > d:
                    html_list.append("</ul>"); depth -= 1
                html_list.append("<li>" + inline(lines[i].strip()[2:]) + "</li>"); i += 1
            html_list += ["</ul>"] * (depth + 1)
            out.append("".join(html_list)); continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"(#{2,4} |\||\s*- )", lines[i]):
            para.append(lines[i].strip()); i += 1
        out.append(f'<p class="mb-2">{inline(" ".join(para))}</p>')
    return "\n".join(out)

if __name__ == "__main__":
    print(render(open(sys.argv[1]).read()))
