"""Render the Markdown used in docs/spec/ to HTML for Lavish review boards.

Covers what the specification uses: headings (with anchors), paragraphs, nested bullet and
numbered lists, tables, block quotes, inline code, bold, italics and links.
"""
import html
import re
import sys


def slug(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\- ]", "", text.lower()).strip()
    return re.sub(r"[ ]+", "-", text)


def inline(t):
    t = html.escape(t, quote=False)
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    t = re.sub(r"`([^`]+)`", keep, t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a class="link" href="\2">\1</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])_([^_]+)_(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", t)
    return t.replace("\\|", "|")


LIST_ITEM = re.compile(r"(\s*)(- |\d+\. )(.*)")


def render_list(lines, i):
    """Render a run of list lines starting at i; returns (html, next index)."""
    out, stack = [], []  # stack of (indent, tag)
    while i < len(lines):
        line = lines[i]
        m = LIST_ITEM.match(line)
        if not m:
            if line.startswith("  ") and line.strip() and stack:
                out.append(" " + inline(line.strip()))
                i += 1
                continue
            break
        indent = len(m.group(1))
        tag = "ol" if m.group(2)[0].isdigit() else "ul"
        while stack and stack[-1][0] > indent:
            out.append(f"</li></{stack.pop()[1]}>")
        if not stack or stack[-1][0] < indent:
            cls = "list-decimal" if tag == "ol" else "list-disc"
            start = ""
            if tag == "ol":
                start = f' start="{int(m.group(2)[:-2])}"'
            out.append(f'<{tag} class="{cls} ml-6 space-y-1"{start}>')
            stack.append((indent, tag))
        else:
            out.append("</li>")
        out.append("<li>" + inline(m.group(3)))
        i += 1
    while stack:
        out.append(f"</li></{stack.pop()[1]}>")
    return "".join(out), i


def render(md):
    out, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"(#{1,4}) (.*)", line)
        if m:
            level = len(m.group(1))
            size = {1: "text-4xl", 2: "text-2xl", 3: "text-xl", 4: "text-lg"}[level]
            text = inline(m.group(2))
            out.append(f'<h{level} id="{slug(text)}" class="{size} font-bold mt-6 mb-3">{text}</h{level}>')
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split(" | ")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            body = "".join(
                "<tr>" + "".join(f'<td class="align-top">{inline(c)}</td>' for c in r) + "</tr>" for r in rows[1:]
            )
            out.append(
                f'<div class="overflow-x-auto mb-4"><table class="table table-sm"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
            )
            continue
        if line.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> ").strip())
                i += 1
            out.append(f'<blockquote class="quote mb-4">{inline(" ".join(quote))}</blockquote>')
            continue
        if LIST_ITEM.match(line):
            html_list, i = render_list(lines, i)
            out.append(f'<div class="mb-4">{html_list}</div>')
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"(#{1,4} |\||>)", lines[i]) and not LIST_ITEM.match(lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append(f'<p class="mb-3">{inline(" ".join(para))}</p>')
    return "\n".join(out)


if __name__ == "__main__":
    print(render(open(sys.argv[1]).read()))
