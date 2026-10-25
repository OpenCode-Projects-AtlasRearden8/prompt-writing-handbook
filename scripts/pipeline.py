#!/usr/bin/env python3
"""Build a static HTML site from the Markdown chapters in docs/.

Standard library only: no installs, no network, works offline.

Usage:
  python3 scripts/pipeline.py                          build docs/ into site/
  python3 scripts/pipeline.py --docs D --out O         custom paths
  python3 scripts/pipeline.py --from-md FILE           print one file as HTML
  python3 scripts/pipeline.py --check                  lint docs (links + anchors)
  python3 scripts/pipeline.py --cards                  print the extracted pattern cards
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
import unicodedata
from pathlib import Path

BOOK_TITLE = "The Prompt-Writing Handbook"
BOOK_SUBTITLE = "Write prompts like a friend would teach you"
BOOK_OWNER = "Asdale Dynamics, LLC"
BOOK_VERSION = "1.0.0"
BOOK_LICENSE = "MIT"
AUTHOR_SITE = "https://dylanasdale.github.io"
TAGLINE = (
    "Why prompts fail, the role/context/format skeleton, few-shot examples, "
    "twelve reusable pattern cards, six before/after rewrites, a plain-file "
    "prompt library, and safe testing against your own local model."
)
CARD_STEM = "05-pattern-cards"

STYLE_CSS = """\
:root {
  --bg: #f7f2ea;
  --panel: #fffdf7;
  --ink: #2b2420;
  --muted: #6f6357;
  --line: #e6dbc9;
  --accent: #8a3d72;
  --accent-soft: #f4e7f0;
  --code-bg: #2c2029;
  --code-ink: #f2e8ee;
  --code-inline: #5e3350;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 17px;
  line-height: 1.65;
}
a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 2px; }
a:hover { text-decoration-thickness: 2px; }
code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
  font-size: 0.88em;
  background: #f0e8e2;
  color: var(--code-inline);
  padding: 0.12em 0.35em;
  border-radius: 5px;
}
pre {
  background: var(--code-bg);
  color: var(--code-ink);
  padding: 1em 1.2em;
  border-radius: 10px;
  overflow-x: auto;
  line-height: 1.5;
  font-size: 0.86em;
}
pre code { background: none; color: inherit; padding: 0; font-size: 1em; }
blockquote {
  margin: 1.2em 0;
  padding: 0.7em 1.1em;
  border-left: 4px solid var(--accent);
  background: var(--accent-soft);
  border-radius: 0 10px 10px 0;
}
blockquote p { margin: 0.35em 0; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1.2em 0;
  background: var(--panel);
  font-size: 0.95em;
}
th, td { border: 1px solid var(--line); padding: 0.55em 0.8em; text-align: left; vertical-align: top; }
th { background: var(--accent-soft); }
li.task { list-style: none; position: relative; padding-left: 1.7em; }
li.task::before {
  content: "";
  position: absolute;
  left: 0.1em; top: 0.28em;
  width: 0.95em; height: 0.95em;
  border: 2px solid var(--accent);
  border-radius: 4px;
}
li.task.done { color: var(--muted); }
li.task.done::before { background: var(--accent); }
li.task.done::after {
  content: "";
  position: absolute;
  left: 0.2em; top: 0.42em;
  width: 0.55em; height: 0.28em;
  border: solid var(--panel);
  border-width: 0 0 2px 2px;
  transform: rotate(-45deg);
}
li.task input { display: none; }
ul ul, ol ol, ul ol, ol ul { margin-top: 0.25em; margin-bottom: 0.25em; }
li { margin: 0.35em 0; }
hr { border: none; border-top: 1px solid var(--line); margin: 2em 0; }

.topbar {
  background: var(--panel);
  border-bottom: 1px solid var(--line);
  padding: 0.6em 1em;
  display: flex;
  flex-wrap: wrap;
  gap: 0.3em 1.2em;
  align-items: baseline;
  position: sticky;
  top: 0;
  z-index: 5;
}
.topbar a { text-decoration: none; color: var(--ink); }
.topbar a:hover { color: var(--accent); }
.topbar .brand { font-weight: 700; }
.topbar .menu { margin-left: auto; }
.topbar .menu a { margin-left: 0.9em; color: var(--muted); }
.topbar .menu a:hover { color: var(--accent); }

.layout { display: flex; align-items: flex-start; max-width: 1200px; margin: 0 auto; }
aside {
  width: 260px;
  flex: 0 0 260px;
  padding: 1.6em 1em 3em 1.4em;
  border-right: 1px solid var(--line);
  font-size: 0.9em;
  position: sticky;
  top: 0;
  max-height: 100vh;
  overflow-y: auto;
}
aside .nav-head {
  font-weight: 700;
  font-size: 0.82em;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 0.6em;
}
aside ol { list-style: none; margin: 0; padding: 0; }
aside li { margin: 0.15em 0; }
aside a { text-decoration: none; color: var(--ink); display: block; padding: 0.28em 0.55em; border-radius: 7px; }
aside a:hover { background: var(--accent-soft); color: var(--accent); }
aside li.current a { background: var(--accent-soft); color: var(--accent); font-weight: 600; }
aside .card-links { margin-top: 1.2em; }
main { flex: 1 1 auto; min-width: 0; padding: 2em 1.5em 4em; }
article {
  max-width: 46rem;
  margin: 0 auto;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 2.2em 2.4em 2.8em;
}
article h1 { font-size: 1.85em; line-height: 1.25; margin-top: 0; }
article h2 { margin-top: 1.7em; padding-top: 0.25em; }
article h2, article h3, article h4 { line-height: 1.3; }
.kicker { color: var(--muted); font-size: 0.9em; margin-bottom: 0.2em; }
.pager { display: flex; justify-content: space-between; gap: 1em; margin-top: 2em; max-width: 46rem; margin-left: auto; margin-right: auto; }
.pager a { text-decoration: none; background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 0.55em 0.95em; }
.pager a:hover { border-color: var(--accent); color: var(--accent); }
.pager .sp { flex: 1; }
.book-toc { max-width: 46rem; margin: 0 auto 2em; }
.book-toc ol { columns: 2; column-gap: 2em; list-style-position: inside; padding-left: 1em; }
.book-toc a { text-decoration: none; }
.cards-grid { max-width: 46rem; margin: 0 auto; }
.cards-grid .card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 0.9em 1.2em;
  margin: 0.8em 0;
}
.cards-grid .card .name { font-weight: 600; }
.cards-grid .card .name a { text-decoration: none; }
.cards-grid .card .use { color: var(--muted); font-size: 0.93em; margin: 0.3em 0 0; }
.cards-intro { max-width: 46rem; margin: 0 auto 1.4em; color: var(--muted); }

footer.site {
  border-top: 1px solid var(--line);
  color: var(--muted);
  padding: 1.2em;
  text-align: center;
  font-size: 0.85em;
  background: var(--panel);
}
footer.site a { color: var(--muted); }

.hero { text-align: center; padding: 3em 1em 2em; }
.hero h1 { font-size: 2.3em; margin: 0.2em 0; }
.hero .sub { color: var(--muted); font-size: 1.12em; max-width: 40em; margin: 0 auto 1.4em; }
.hero .btn {
  display: inline-block;
  background: var(--accent);
  color: #ffffff;
  text-decoration: none;
  font-weight: 600;
  padding: 0.65em 1.5em;
  border-radius: 999px;
  margin: 0.3em;
}
.hero .btn:hover { filter: brightness(1.08); }
.hero .btn.ghost { background: none; color: var(--accent); border: 1px solid var(--accent); }
.hero pre { max-width: 40em; margin: 1.6em auto 1.2em; text-align: left; }
.hero small { color: var(--muted); }

.toc { max-width: 46rem; margin: 1em auto 3em; padding: 0 1em; }
.toc ol { list-style: none; padding: 0; margin: 0; }
.toc li {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 0.9em 1.2em;
  margin: 0.7em 0;
}
.toc a { text-decoration: none; font-weight: 600; display: block; }
.toc .desc { color: var(--muted); font-weight: 400; font-size: 0.93em; margin: 0.25em 0 0; }
.toc .num { color: var(--accent); font-variant-numeric: tabular-nums; margin-right: 0.4em; }

@media (max-width: 900px) {
  .layout { display: block; }
  aside { position: static; width: auto; max-height: none; border-right: none; border-bottom: 1px solid var(--line); }
  article { padding: 1.6em 1.2em 2em; border-radius: 0; border-left: none; border-right: none; }
  .book-toc ol { columns: 1; }
}
@media print {
  body { background: #ffffff; }
  .topbar, aside, .pager, footer.site, .hero { display: none; }
  article { border: none; background: #ffffff; padding: 0; }
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1417;
    --panel: #231c20;
    --ink: #ece0e6;
    --muted: #ab9aa4;
    --line: #382b33;
    --accent: #d982b6;
    --accent-soft: #35212e;
    --code-bg: #120d10;
    --code-ink: #ece0e6;
    --code-inline: #dcb3c8;
  }
  .hero .btn { color: #16100f; }
  .hero .btn.ghost { color: var(--accent); }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
}
"""

MENU_LINKS = (
    '<a href="index.html">Start here</a>'
    '<a href="cards.html">Pattern cards</a>'
    '<a href="book.html">Whole book</a>'
    f'<a href="{AUTHOR_SITE}">Author site</a>'
)

PAGE_TMPL = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="style.css">{meta}
<title>{title} | {book}</title>
</head>
<body>
<header class="topbar">
  <a class="brand" href="index.html">{brand}</a>
  <nav class="menu">{menu}</nav>
</header>
<div class="layout">
{nav}
<main>
<article>
{content}
</article>
</main>
</div>
<footer class="site">
  <p>{book} | a beginner guide from {owner}</p>
  <p>Built locally by <code>scripts/pipeline.py</code> with no tracking, no accounts, and no network calls, so it works offline. {license} licensed. Version {version}.</p>
</footer>
</body>
</html>
"""

HOME_TMPL = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{tagline}">
<link rel="stylesheet" href="style.css">
<title>{book} | {subtitle}</title>
</head>
<body>
<header class="topbar">
  <a class="brand" href="index.html">{brand}</a>
  <nav class="menu">{menu}</nav>
</header>
<div class="hero">
  <p class="kicker">A free, plain-English guide by {owner}</p>
  <h1>{book}</h1>
  <p class="sub">{tagline}</p>
  <p><a class="btn" href="{first_href}">Start reading</a> <a class="btn ghost" href="cards.html">Browse the pattern cards</a> <a class="btn ghost" href="book.html">Read or print the whole book</a></p>
<pre><code>python3 -m promptlab run everyday-explainer --input "what a token is"
# offline, on your own machine, no key, no bill</code></pre>
  <p><small>That command is the companion tool, Prompt Lab. This book teaches
  the writing half of the pair: how to make the prompt worth running.</small></p>
</div>
<div class="toc">
  <ol>
{toc_items}
  </ol>
</div>
<footer class="site">
  <p>{book} | a beginner guide from {owner}</p>
  <p>{license} licensed. Version {version}. Copy it, share it, tinker with it.</p>
</footer>
</body>
</html>
"""

SENTINEL = "\x00cd{}\x00"
LIST_ITEM = re.compile(r"^(\s*)([-*]|\d+[.)])\s+(.*)$")
TASK_ITEM = re.compile(r"^(\s*)[-*] \[([ xX])\]\s+(.*)$")
HEADING = re.compile(r"^(#{1,6}) (.*)$")
FENCE_OPEN = re.compile(r"^```([^`]*)$")
FENCE_CLOSE = re.compile(r"^```[^`]*$")
TABLE_DIVIDER = re.compile(r"^\|?(\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?$")
LINK_MD = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
EXTERNAL_LINK = re.compile(r"(?i)^https?://")
FRONT_MATTER = re.compile(r"^00[-_]")


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def esc_attr(text: str) -> str:
    return html.escape(text, quote=True)


def slugify(text: str) -> str:
    norm = unicodedata.normalize("NFKD", text)
    ascii_text = norm.encode("ascii", "ignore").decode("ascii").lower()
    words = re.findall(r"[a-z0-9]+", ascii_text)
    return "-".join(words) or "section"


def plain_text(markdown: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", markdown)
    text = LINK_MD.sub(r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"\1", text)
    return text.strip()


def _href_for(target: str) -> str:
    if EXTERNAL_LINK.match(target):
        return esc_attr(target)
    path_part, _, frag = target.partition("#")
    if path_part.endswith(".md"):
        path_part = out_name(path_part.rstrip("/")[:-3])
    if path_part or frag:
        return esc_attr((path_part + "#" + frag) if frag else path_part)
    return esc_attr(target)


def inline(markdown: str, stash: list[str]) -> str:
    def stash_code(match: re.Match) -> str:
        stash.append(match.group(1))
        return SENTINEL.format(len(stash) - 1)

    def replace_link(match: re.Match) -> str:
        label, target = match.group(1), match.group(2)
        return f'<a href="{_href_for(target)}">{label}</a>'

    def restore(match: re.Match) -> str:
        return "<code>" + esc(stash[int(match.group(1))]) + "</code>"

    text = re.sub(r"`([^`\n]+)`", stash_code, markdown)
    text = esc(text)
    text = LINK_MD.sub(replace_link, text)
    text = re.sub(r"\*\*([^*\n]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(SENTINEL.format(r"(\d+)"), restore, text)
    return text


def _parse_list_block(lines: list[str], i: int) -> tuple[list[tuple[int, str, bool, bool, str]], int]:
    items: list[tuple[int, str, bool, bool, str]] = []
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            break
        task = TASK_ITEM.match(line)
        bullet = LIST_ITEM.match(line)
        if task:
            indent = len(task.group(1))
            body = task.group(3)
            kind = "ul"
            checked = task.group(2).lower() == "x"
            items.append((indent, kind, True, checked, body))
        elif bullet:
            indent = len(bullet.group(1))
            kind = "ol" if bullet.group(2)[0].isdigit() else "ul"
            items.append((indent, kind, False, False, bullet.group(3)))
        else:
            break
        i += 1
    return items, i


def _render_children(nodes: list[dict], stash: list[str]) -> str:
    htmls: list[str] = []
    group: list[dict] = []
    for node in nodes + [None]:
        tag = node["tag"] if node else None
        if group and (tag != group[0]["tag"] or node is None):
            items = []
            for item in group:
                sub = _render_children(item["children"], stash) if item["children"] else ""
                if item["task"]:
                    checked = " checked" if item["checked"] else ""
                    items.append(
                        f'<li class="task{" done" if item["checked"] else ""}">'
                        f'<input type="checkbox"{checked} disabled> {inline(item["body"], stash)}{sub}</li>'
                    )
                else:
                    items.append(f"<li>{inline(item['body'], stash)}{sub}</li>")
            t = group[0]["tag"]
            htmls.append(f"<{t}>\n" + "\n".join(items) + f"\n</{t}>")
            group = []
        if node is not None:
            group.append(node)
    return "".join(htmls)


def _convert_lists(lines: list[str], i: int, stash: list[str]) -> tuple[str, int]:
    flat, end = _parse_list_block(lines, i)
    if not flat:
        raise ValueError(f"unparsable list line: {lines[i]!r}")
    root: dict = {"indent": -1, "children": []}
    stack = [root]
    for indent, kind, task, checked, body in flat:
        while len(stack) > 1 and stack[-1]["indent"] >= indent:
            stack.pop()
        parent = stack[-1]
        node = {
            "indent": indent,
            "tag": "ol" if kind == "ol" else "ul",
            "task": task,
            "checked": checked,
            "body": body,
            "children": [],
        }
        parent["children"].append(node)
        stack.append(node)
    return _render_children(root["children"], stash), end - i


def _table_html(start: int, lines: list[str], stash: list[str]) -> tuple[str, int]:
    header = lines[start]
    headers = _table_cells(header)
    rows: list[str] = []
    end = start + 2
    while end < len(lines) and lines[end].strip() and lines[end].lstrip().startswith("|"):
        cells = _table_cells(lines[end])
        if len(cells) < len(headers):
            cells += [""] * (len(headers) - len(cells))
        row = "".join(f"<td>{inline(cell, stash)}</td>" for cell in cells[: len(headers)])
        rows.append(f"<tr>{row}</tr>")
        end += 1
    head = "".join(f"<th>{inline(cell, stash)}</th>" for cell in headers)
    body = "".join(f"\n{row}" for row in rows)
    return (
        f'<table>\n<thead>\n<tr>{head}</tr>\n</thead>\n<tbody>{body}\n</tbody>\n</table>',
        end - start,
    )


def _table_cells(row: str) -> list[str]:
    trimmed = row.strip()
    if trimmed.startswith("|"):
        trimmed = trimmed[1:]
    if trimmed.endswith("|"):
        trimmed = trimmed[:-1]
    return [cell.strip() for cell in trimmed.split("|")]


def convert(markdown: str) -> str:
    stash: list[str] = []
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: list[str] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            out.append("<p>" + inline(" ".join(paragraph), stash) + "</p>")
            paragraph.clear()

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        fence = FENCE_OPEN.match(stripped)
        if fence:
            flush_paragraph()
            lang = fence.group(1).strip()
            i += 1
            body: list[str] = []
            while i < n and not FENCE_CLOSE.match(lines[i].strip()):
                body.append(lines[i])
                i += 1
            i += 1
            cls = f' class="lang-{slugify(lang)}"' if lang else ""
            out.append(f"<pre{cls}><code>" + esc("\n".join(body)) + "</code></pre>")
            continue

        if not stripped:
            flush_paragraph()
            i += 1
            continue

        heading = HEADING.match(stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            text = heading.group(2).strip()
            out.append(f'<h{level} id="{slugify(text)}">{inline(text, stash)}</h{level}>')
            i += 1
            continue

        if stripped in {"---", "***", "___"}:
            flush_paragraph()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            quote: list[str] = []
            while i < n and lines[i].lstrip().startswith(">"):
                quote.append(lines[i].lstrip()[1:].strip())
                i += 1
            out.append("<blockquote>\n<p>" + inline(" ".join(quote), stash) + "</p>\n</blockquote>")
            continue

        if stripped.startswith("|") and i + 1 < n and TABLE_DIVIDER.match(lines[i + 1].strip()):
            flush_paragraph()
            table, used = _table_html(i, lines, stash)
            out.append(table)
            i += used
            continue

        if TASK_ITEM.match(line) or LIST_ITEM.match(line):
            flush_paragraph()
            rendered, used = _convert_lists(lines, i, stash)
            out.append(rendered)
            i += used
            continue

        paragraph.append(stripped)
        i += 1

    flush_paragraph()
    return "\n".join(out)


def out_name(stem: str) -> str:
    return re.sub(r"^\d+[-_]", "", stem) + ".html"


def doc_title(text: str) -> str:
    for line in text.splitlines():
        heading = re.match(r"^#\s+(.+)$", line.strip())
        if heading:
            return heading.group(1).strip()
    raise ValueError("missing first-level title")


def doc_summary(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        return plain_text(stripped)
    return ""


def doc_heading_slugs(text: str) -> set[str]:
    slugs = set()
    for line in text.splitlines():
        heading = HEADING.match(line.strip())
        if heading:
            slugs.add(slugify(heading.group(2).strip()))
    return slugs


def extract_pattern_cards(text: str) -> list[dict]:
    """Pull the fill-in-the-blank pattern cards out of a chapter's markdown.

    A card is an h2 heading beginning with "Card:" followed by its intro
    paragraph (the "For: ..." line). Returns dicts with slug, title, use.
    """
    cards: list[dict] = []
    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines):
        heading = HEADING.match(lines[i].strip())
        if heading and len(heading.group(1)) == 2 and heading.group(2).strip().lower().startswith("card:"):
            title = heading.group(2).strip()
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            para: list[str] = []
            while j < len(lines) and lines[j].strip() and not lines[j].strip().startswith(("#", "```", "|", ">")):
                para.append(lines[j].strip())
                j += 1
            cards.append(
                {
                    "slug": slugify(title),
                    "title": title,
                    "use": plain_text(" ".join(para)) if para else "",
                }
            )
        i += 1
    return cards


def _chapter_numbers(chapters: list[dict]) -> None:
    """Give each chapter a book number; '00-' stems are front matter (intro)."""
    total = sum(1 for c in chapters if not FRONT_MATTER.match(c["stem"]))
    n = 0
    for c in chapters:
        if FRONT_MATTER.match(c["stem"]):
            c["num"] = None
        else:
            n += 1
            c["num"] = n
    for c in chapters:
        c["total"] = total


def _kicker(ch: dict) -> str:
    if ch["num"] is None:
        return "Front matter — read this first"
    return f"Chapter {ch['num']} of {ch['total']}"


def lint_docs(docs: list[tuple[str, str]]) -> list[str]:
    problems: list[str] = []
    slugs_by_file: dict[str, set[str]] = {}
    name_by_file: dict[str, str] = {}
    for stem, text in docs:
        try:
            title = doc_title(text)
        except ValueError:
            problems.append(f"{stem}.md: no 'title' first-level heading found")
            title = stem
        if len(title) > 90:
            problems.append(f"{stem}.md: title is very long")
        slugs = doc_heading_slugs(text)
        duplicate = len(slugs) < len([1 for line in text.splitlines() if HEADING.match(line.strip())])
        if duplicate:
            problems.append(f"{stem}.md: duplicate heading text would break anchors")
        if stem.startswith("_"):
            problems.append(f"{stem}.md: files starting with underscore are skipped from the build")
        slugs_by_file[stem] = slugs
        name_by_file[stem] = out_name(stem)
    seen_names: dict[str, str] = {}
    for stem, name in name_by_file.items():
        if name in seen_names:
            problems.append(f"{stem}.md: output name {name} collides with {seen_names[name]}")
        seen_names[name] = stem
    for stem, text in docs:
        for match in LINK_MD.finditer(text):
            target = match.group(2)
            if EXTERNAL_LINK.match(target):
                continue
            path_part, _, frag = target.partition("#")
            if not path_part.endswith(".md"):
                problems.append(f"{stem}.md: internal link should point at a .md file: {target}")
                continue
            other = path_part[:-3]
            if other not in slugs_by_file:
                problems.append(f"{stem}.md: link target does not exist: {target}")
            elif frag and frag not in slugs_by_file[other]:
                problems.append(f"{stem}.md: anchor not found in {other}.md: #{frag}")
    card_stems = [stem for stem, _ in docs if stem == CARD_STEM]
    if card_stems:
        cards = extract_pattern_cards(dict(docs)[CARD_STEM])
        named = [c for c in cards if c["use"]]
        if len(named) != len(cards):
            problems.append(f"{CARD_STEM}.md: every card heading must be followed by its 'For:' paragraph")
        if len(cards) < 4:
            problems.append(f"{CARD_STEM}.md: expected at least 4 pattern cards, found {len(cards)}")
    return problems


def build_site(docs_dir: Path, out_dir: Path) -> list[Path]:
    docs_dir, out_dir = docs_dir.resolve(), out_dir.resolve()
    if out_dir == Path(out_dir.anchor) or out_dir in (docs_dir, *docs_dir.parents):
        raise ValueError(f"refusing to build into dangerous output path: {out_dir}")
    files = sorted(p for p in docs_dir.glob("*.md") if not p.name.startswith("_"))
    if not files:
        raise SystemExit(f"no markdown chapters found in {docs_dir}")
    docs = [(p.stem, p.read_text(encoding="utf-8")) for p in files]
    problems = lint_docs(docs)
    if problems:
        for problem in problems:
            print("DOC LINT: " + problem, file=sys.stderr)
        raise SystemExit("docs failed lint; fix the issues above")

    chapters: list[dict] = []
    for stem, text in docs:
        title = doc_title(text)
        chapters.append(
            {
                "stem": stem,
                "name": out_name(stem),
                "title": title,
                "plain": plain_text(title),
                "summary": doc_summary(text),
                "html": convert(text),
            }
        )
    _chapter_numbers(chapters)

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    nav_items = "".join(
        f'<li><a href="{c["name"]}">{esc(c["plain"])}</a></li>' for c in chapters
    )
    template_vars = {
        "brand": esc(BOOK_TITLE),
        "book": esc(BOOK_TITLE),
        "owner": esc(BOOK_OWNER),
        "version": BOOK_VERSION,
        "license": BOOK_LICENSE,
        "menu": MENU_LINKS,
    }

    written: list[Path] = []
    for idx, chapter in enumerate(chapters):
        meta = ""
        if chapter["summary"]:
            desc = chapter["summary"][:150] + ("..." if len(chapter["summary"]) > 150 else "")
            meta = f'\n<meta name="description" content="{esc_attr(desc)}">'
        nav = f'<aside>\n<p class="nav-head">Chapters</p>\n<ol>\n{nav_items}\n</ol>\n</aside>'
        content = f'<p class="kicker">{_kicker(chapter)}</p>\n' + chapter["html"]
        prev_ch = chapters[idx - 1] if idx else None
        next_ch = chapters[idx + 1] if idx + 1 < len(chapters) else None
        parts = []
        if prev_ch:
            parts.append(
                f'<a href="{prev_ch["name"]}">&larr; {esc(plain_text(prev_ch["title"]))}</a>'
            )
        else:
            parts.append('<a href="index.html">&larr; Start here</a>')
        parts.append('<span class="sp"></span>')
        if next_ch:
            parts.append(
                f'<a href="{next_ch["name"]}">{esc(plain_text(next_ch["title"]))} &rarr;</a>'
            )
        content += '\n<div class="pager">' + "".join(parts) + "</div>"
        page = PAGE_TMPL.format(
            meta=meta,
            title=esc(
                chapter["plain"]
                if chapter["num"] is None
                else chapter["plain"] + " | Chapter " + str(chapter["num"])
            ),
            content=content,
            nav=nav,
            **template_vars,
        )
        path = out_dir / chapter["name"]
        path.write_text(page, encoding="utf-8")
        written.append(path)

    doc_text_by_stem = dict(docs)
    cards = extract_pattern_cards(doc_text_by_stem.get(CARD_STEM, "")) if CARD_STEM in doc_text_by_stem else []
    if cards:
        cards_page_name = out_name(CARD_STEM)
        card_html_items = "".join(
            f'<div class="card" id="pc-{c["slug"]}">'
            f'<p class="name"><a href="{cards_page_name}#{c["slug"]}">{esc(c["title"])}</a></p>'
            f'<p class="use">{esc_attr(c["use"])}</p></div>'
            for c in cards
        )
        cards_page = PAGE_TMPL.format(
            meta='\n<meta name="description" content="All twelve pattern cards on one page: fill-in-the-blank prompt recipes.">',
            title="Pattern cards",
            nav=f'<aside>\n<p class="nav-head">Chapters</p>\n<ol>\n{nav_items}\n</ol>\n</aside>',
            content=(
                '<h1 style="margin-top:0">Pattern cards</h1>'
                '<p class="cards-intro">Twelve fill-in-the-blank prompt recipes, copied from '
                f'<a href="{cards_page_name}">the pattern cards chapter</a>. Click a card to read '
                "its skeleton and a worked example there.</p>"
                '<div class="cards-grid">\n' + card_html_items + "\n</div>"
            ),
            **template_vars,
        )
        cards_path = out_dir / "cards.html"
        cards_path.write_text(cards_page, encoding="utf-8")
        written.append(cards_path)

    book_sections: list[str] = []
    book_toc: list[str] = []
    for chapter in chapters:
        section_id = "front" if chapter["num"] is None else f"ch-{chapter['num']}"
        book_toc.append(f'<li><a href="#{section_id}">{esc(chapter["plain"])}</a></li>')
        book_sections.append(
            f'<hr>\n<section id="{section_id}">\n<p class="kicker">{_kicker(chapter)}</p>\n'
            + chapter["html"]
            + "\n</section>"
        )
    book_content = (
        '<div class="book-toc"><ol>\n' + "\n".join(book_toc) + "\n</ol></div>"
        + "".join(book_sections)
    )
    book_page = PAGE_TMPL.format(
        meta='\n<meta name="description" content="The whole book on one page, ready to search or print.">',
        title="Whole book",
        content=book_content,
        nav=f'<aside>\n<p class="nav-head">Chapters</p>\n<ol>\n{nav_items}\n</ol>\n</aside>',
        **template_vars,
    )
    book_path = out_dir / "book.html"
    book_path.write_text(book_page, encoding="utf-8")
    written.append(book_path)

    toc_items = "".join(
        f'    <li><a href="{c["name"]}"'
        f'><span class="num">{"FM" if c["num"] is None else format(c["num"], "02d")}</span>{esc(c["plain"])}</a>'
        f'<p class="desc">{esc(c["summary"])}</p></li>'
        for c in chapters
    )
    home = HOME_TMPL.format(
        tagline=esc_attr(TAGLINE),
        subtitle=esc(BOOK_SUBTITLE),
        first_href=chapters[0]["name"],
        toc_items=toc_items,
        **template_vars,
    )
    home_path = out_dir / "index.html"
    home_path.write_text(home, encoding="utf-8")
    written.append(home_path)

    css_path = out_dir / "style.css"
    css_path.write_text(STYLE_CSS, encoding="utf-8")
    written.append(css_path)
    return written


def print_html(markdown: str) -> None:
    sys.stdout.write(convert(markdown) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--docs", default=None, help="docs directory with the markdown book")
    parser.add_argument("--out", default=None, help="output directory for the static site")
    parser.add_argument("--from-md", default=None, help="convert one markdown file and print HTML")
    parser.add_argument("--cards", action="store_true", help="print the extracted pattern cards and exit")
    parser.add_argument("--check", action="store_true", help="lint docs and exit")
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parent.parent
    if args.from_md:
        path = Path(args.from_md).resolve()
        if not path.is_file():
            raise SystemExit(f"file not found: {path}")
        print_html(path.read_text(encoding="utf-8"))
        return 0
    docs_dir = Path(args.docs).resolve() if args.docs else root / "docs"
    out_dir = Path(args.out).resolve() if args.out else root / "site"
    if args.cards:
        path = docs_dir / f"{CARD_STEM}.md"
        if not path.is_file():
            raise SystemExit(f"file not found: {path}")
        cards = extract_pattern_cards(path.read_text(encoding="utf-8"))
        for card in cards:
            slug = card["slug"]
            title = card["title"]
            use = card["use"]
            print(f"* {title} [#{slug}] {use}")
        if not cards:
            print("no pattern cards found; check CARD_STEM", file=sys.stderr)
            return 1
        return 0
    if args.check:
        files = sorted(p for p in docs_dir.glob("*.md") if not p.name.startswith("_"))
        docs = [(p.stem, p.read_text(encoding="utf-8")) for p in files]
        problems = lint_docs(docs)
        for problem in problems:
            print("DOC LINT: " + problem, file=sys.stderr)
        print(f"Checked {len(docs)} markdown files: {'clean' if not problems else f'{len(problems)} problem(s)'}")
        return 1 if problems else 0
    written = build_site(docs_dir, out_dir)
    print(f"Built {len(written)} files into {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
