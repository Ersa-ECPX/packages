"""Markdown to HTML for the packages site. A copy of the converter in ecp-mkosi/scripts/build-wiki (kept identical on purpose:
the two sites render the same documents the same way), so that this repository builds on its own.

It handles exactly what the documents use (headings, paragraphs, fenced code, tables, nested lists, emphasis, code spans, links,
rules) and escapes all other HTML.
"""

import html
import re

LIST_ITEM = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")
TABLE_SEPARATOR = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")


def slug(text):
    text = re.sub(r"<[^>]+>|[`*_]", "", text).lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text.strip()) or "section"


class Converter:
    """Markdown to HTML for one page. `resolve(href)` maps a link target to (href, is_page) or None."""

    def __init__(self, resolve):
        self.resolve = resolve
        self.headings, self.title, self.used = [], "", {}

    # inline
    def inline(self, text):
        pictures = []

        def picture(match):
            pictures.append(self._image(match))
            return f"\x03{len(pictures) - 1}\x03"
        text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", picture, text)
        codes = []

        def stash(match):
            codes.append(match.group(2))
            return f"\x00{len(codes) - 1}\x00"
        text = re.sub(r"(`+)(.+?)\1", stash, text)
        text = html.escape(text, quote=False)
        text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", self._link, text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
        text = re.sub(r"\x00(\d+)\x00", lambda m: "<code>" + html.escape(codes[int(m.group(1))], quote=False) + "</code>", text)
        return re.sub(r"\x03(\d+)\x03", lambda m: pictures[int(m.group(1))], text)

    def _image(self, match):
        alt, target = match.group(1), html.unescape(match.group(2))
        source = self.resolve_image(target) if getattr(self, "resolve_image", None) else None
        if source is None:
            return f'<span class="filelink" title="{html.escape(target)}">[image: {html.escape(alt)}]</span>'
        return f'<img src="{html.escape(source)}" alt="{html.escape(alt)}" loading="lazy">'

    def _link(self, match):
        label, target = match.group(1), html.unescape(match.group(2))
        if re.match(r"^[a-z][a-z0-9+.-]*:", target):                  # an absolute URL
            return f'<a href="{html.escape(target)}" rel="noopener">{label}</a>'
        resolved = self.resolve(target)
        if resolved is None:
            return f'<span class="filelink" title="{html.escape(target)}">{label}</span>'
        return f'<a href="{html.escape(resolved)}">{label}</a>'

    # blocks
    def convert(self, text):
        lines = text.replace("\r\n", "\n").split("\n")
        return self.blocks(lines)

    def heading_id(self, title, explicit=None):
        base = explicit or slug(title)
        count = self.used.get(base, 0)
        self.used[base] = count + 1
        return base if count == 0 else f"{base}-{count}"

    def blocks(self, lines):
        out, i, n = [], 0, len(lines)
        while i < n:
            line = lines[i]
            if not line.strip():
                i += 1
            elif line.startswith("```"):
                language, i = line[3:].strip(), i + 1
                body = []
                while i < n and not lines[i].startswith("```"):
                    body.append(lines[i])
                    i += 1
                i += 1
                out.append(f'<pre><button class="copy" type="button">Copy</button><code>{html.escape(chr(10).join(body), quote=False)}</code></pre>')
            elif re.match(r"^#{1,6}\s", line):
                level = len(line) - len(line.lstrip("#"))
                raw = line[level:].strip()
                anchor = re.search(r'<a id="([^"]+)"></a>', raw)
                raw = re.sub(r'<a id="[^"]+"></a>', "", raw).strip()
                ident = self.heading_id(raw, anchor.group(1) if anchor else None)
                if level == 1 and not self.title:
                    self.title = re.sub(r"[`*]", "", raw)
                self.headings.append((level, re.sub(r"[`*]", "", raw), ident))
                out.append(f'<h{level} id="{ident}">{self.inline(raw)}</h{level}>')
                i += 1
            elif re.match(r"^---+\s*$", line):
                out.append("<hr>")
                i += 1
            elif line.lstrip().startswith("|") and i + 1 < n and TABLE_SEPARATOR.match(lines[i + 1]):
                html_table, i = self.table(lines, i)
                out.append(html_table)
            elif LIST_ITEM.match(line):
                html_list, i = self.list(lines, i)
                out.append(html_list)
            else:
                paragraph = [line.strip()]
                i += 1
                while i < n and lines[i].strip() and not self._starts_block(lines, i):
                    paragraph.append(lines[i].strip())
                    i += 1
                rendered = self.inline(" ".join(paragraph))
                only = re.fullmatch(r'(<img [^>]*alt="([^"]*)"[^>]*>)', rendered)
                if only:
                    caption = f"<figcaption>{only.group(2)}</figcaption>" if only.group(2) else ""
                    out.append(f"<figure>{only.group(1)}{caption}</figure>")
                else:
                    out.append(f"<p>{rendered}</p>")
        return "\n".join(out)

    @staticmethod
    def _starts_block(lines, i):
        line = lines[i]
        return (line.startswith("```") or re.match(r"^#{1,6}\s", line) or LIST_ITEM.match(line)
                or re.match(r"^---+\s*$", line)
                or (line.lstrip().startswith("|") and i + 1 < len(lines) and TABLE_SEPARATOR.match(lines[i + 1])))

    @staticmethod
    def split_row(line):
        """Cells of a table row; a `|` inside a code span or escaped as \\| belongs to the cell."""
        line = line.strip()
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|") and not line.endswith("\\|"):
            line = line[:-1]
        cells, current, in_code, i = [], [], False, 0
        while i < len(line):
            char = line[i]
            if char == "\\" and i + 1 < len(line) and line[i + 1] == "|":
                current.append("|")
                i += 2
                continue
            if char == "`":
                in_code = not in_code
            if char == "|" and not in_code:
                cells.append("".join(current).strip())
                current = []
            else:
                current.append(char)
            i += 1
        cells.append("".join(current).strip())
        return cells

    def table(self, lines, i):
        header = self.split_row(lines[i])
        alignments = []
        for cell in self.split_row(lines[i + 1]):
            left, right = cell.startswith(":"), cell.endswith(":")
            alignments.append("center" if left and right else "right" if right else "left" if left else "")
        i += 2
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            rows.append(self.split_row(lines[i]))
            i += 1

        def cell(tag, text, column):
            style = f' style="text-align:{alignments[column]}"' if column < len(alignments) and alignments[column] else ""
            return f"<{tag}{style}>{self.inline(text)}</{tag}>"
        head = "".join(cell("th", text, c) for c, text in enumerate(header))
        body = "".join("<tr>" + "".join(cell("td", text, c) for c, text in enumerate(row)) + "</tr>" for row in rows)
        return f'<div class="table"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>', i

    def list(self, lines, i):
        first = LIST_ITEM.match(lines[i])
        indent = len(first.group(1))
        ordered = first.group(2)[0].isdigit()
        items = []
        while i < len(lines):
            match = LIST_ITEM.match(lines[i])
            if not match or len(match.group(1)) != indent:
                break
            width = len(match.group(1)) + len(match.group(2)) + 1
            body = [match.group(3)]
            i += 1
            while i < len(lines):
                line = lines[i]
                if not line.strip():
                    following = next((l for l in lines[i + 1:i + 3] if l.strip()), "")
                    if following.startswith(" " * (width + 1)) or (following and LIST_ITEM.match(following)
                                                                   and len(LIST_ITEM.match(following).group(1)) > indent):
                        body.append("")
                        i += 1
                        continue
                    break
                if len(line) - len(line.lstrip()) > indent and not (LIST_ITEM.match(line) and len(LIST_ITEM.match(line).group(1)) == indent):
                    body.append(line[min(width, len(line) - len(line.lstrip())):] if line.startswith(" " * width) else line.strip())
                    i += 1
                    continue
                break
            items.append(body)
        tag = "ol" if ordered else "ul"
        rendered = []
        for body in items:
            split = next((k for k, l in enumerate(body) if k and LIST_ITEM.match(l)), len(body))
            text = " ".join(l.strip() for l in body[:split] if l.strip())
            nested = self.blocks(body[split:]) if split < len(body) else ""
            rendered.append(f"<li>{self.inline(text)}{nested}</li>")
        return f"<{tag}>" + "".join(rendered) + f"</{tag}>", i
