import io
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
import pipeline


FIXTURE_A = """\
# Alpha Chapter

Hello world with **bold**, *soft*, and `code` here.

- one
- two
  - deep

1. first
2. second

- [ ] todo
- [x] done

> quote line

| A | B |
| --- | --- |
| 1 | 2 |
| x | y |

```bash
echo hi
```

---

Final paragraph linking to [glossary](09-glossary.md#token-plus).
"""

FIXTURE_B = """\
# Glossary Thing

Some intro.

## token plus

Body about tokens.
"""

FIXTURE_CARDS = """\
# Pattern Cards

How to read a card.

## Card: The Alpha Card

For: doing alpha things — home, work, hobbies.

```text
Do [ALPHA] with [BETA].
```

## Card: The Beta Card

For: doing beta things instead. (Borrowed from Chapter 1.)

```text
Try [GAMMA].
```

## Card: The Gamma Card

For: gamma-shaped jobs — quick checks, warm lists, small fixes.

```text
List [DELTA] without explaining why.
```

## Card: The Delta Card

For: delta-shaped jobs too. Keep cards short and re-testable.

```text
Rewrite [EPSILON] in one sentence.
```

## Not A Card Heading

Just prose here.
"""


class ConverterTests(unittest.TestCase):

    def conv_html(self, doc):
        return pipeline.convert(doc)

    def test_headings_and_anchors(self):
        html = self.conv_html("## My Section\nwords")
        self.assertIn('<h2 id="my-section">My Section</h2>', html)

    def test_inline_markers(self):
        html = self.conv_html("dog **bold** cat *soft* end `x` and `y` tail")
        self.assertIn("<strong>bold</strong>", html)
        self.assertIn("<em>soft</em>", html)
        self.assertIn("<code>x</code>", html)
        self.assertIn("<code>y</code>", html)
        self.assertNotIn("**", html)
        self.assertNotIn("*soft*", html)

    def test_html_escapes_but_code_is_literal(self):
        html = self.conv_html("safe <script> tag & `x <b>y</b>` z")
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("<code>x &lt;b&gt;y&lt;/b&gt;</code>", html)
        self.assertNotIn("<script>", html)

    def test_internal_link_rewrite(self):
        html = self.conv_html("see [token](09-glossary.md#token)")
        self.assertIn('<a href="glossary.html#token">token</a>', html)

    def test_external_link_kept(self):
        html = self.conv_html("go [there](https://example.com/a)")
        self.assertIn('href="https://example.com/a"', html)

    def test_lists_nested_and_ordered(self):
        html = self.conv_html("- a\n- b\n  - b1\n1. one\n2. two")
        self.assertIn("<ul>\n<li>a</li>\n<li>b<ul>\n<li>b1</li>\n</ul></li>\n</ul>", html)
        self.assertIn("<ol>\n<li>one</li>\n<li>two</li>\n</ol>", html)

    def test_task_lists(self):
        html = self.conv_html("- [ ] todo\n- [x] done")
        self.assertIn('<li class="task"><input type="checkbox" disabled> todo</li>', html)
        self.assertIn('<li class="task done"><input type="checkbox" checked disabled> done</li>', html)

    def test_blockquote_hr_paragraph_join(self):
        html = self.conv_html("> one line\n\n---\n\nfirst\nsecond")
        self.assertIn("<blockquote>\n<p>one line</p>\n</blockquote>", html)
        self.assertIn("<hr>", html)
        self.assertIn("<p>first second</p>", html)

    def test_table_cells_and_padding(self):
        html = self.conv_html("| A | B |\n| --- | --- |\n| 1 | 2 |\n| short | ")
        self.assertIn("<th>A</th><th>B</th>", html)
        self.assertIn("<td>1</td><td>2</td>", html)
        self.assertIn("<td>short</td><td></td>", html)

    def test_code_fence_language_and_protection(self):
        html = self.conv_html("```bash\nrun --flag `nested`\n```")
        self.assertIn('<pre class="lang-bash"><code>run --flag `nested`</code></pre>', html)

    def test_slugify_ascii(self):
        self.assertEqual(pipeline.slugify("Café Menu — 2!"), "cafe-menu-2")

    def test_plain_text(self):
        self.assertEqual(
            pipeline.plain_text("**Bold** [link](a.md) and `code` rock"),
            "Bold link and code rock",
        )

    def test_doc_title(self):
        self.assertEqual(pipeline.doc_title("pre\n# The Title\n"), "The Title")

    def test_out_name_strips_numbering(self):
        self.assertEqual(pipeline.out_name("09-glossary"), "glossary.html")


class PatternCardTests(unittest.TestCase):

    def test_extracts_cards_with_slugs_and_use_lines(self):
        cards = pipeline.extract_pattern_cards(FIXTURE_CARDS)
        self.assertEqual(
            [c["title"] for c in cards],
            ["Card: The Alpha Card", "Card: The Beta Card", "Card: The Gamma Card", "Card: The Delta Card"],
        )
        self.assertEqual(cards[0]["slug"], "card-the-alpha-card")
        self.assertIn("For: doing alpha things", cards[0]["use"])
        self.assertIn("(Borrowed from Chapter 1.)", cards[1]["use"])

    def test_non_card_headings_ignored(self):
        cards = pipeline.extract_pattern_cards(FIXTURE_CARDS)
        self.assertNotIn("Not A Card Heading", [c["title"] for c in cards])

    def test_use_line_stops_at_fence_or_blank(self):
        markdown = "## Card: X\n\nFor: first line.\nsecond line.\n\n```text\nbody\n```"
        cards = pipeline.extract_pattern_cards(markdown)
        self.assertEqual(cards[0]["use"], "For: first line. second line.")

    def test_repo_book_has_twelve_cards(self):
        root = Path(__file__).resolve().parent.parent
        cards = pipeline.extract_pattern_cards(
            (root / "docs" / "05-pattern-cards.md").read_text(encoding="utf-8")
        )
        self.assertEqual(len(cards), 12, "the book promises twelve cards")
        self.assertTrue(all(c["use"].startswith("For:") for c in cards))


class LintTests(unittest.TestCase):

    def lint(self, pairs, expected_fragment):
        problems = pipeline.lint_docs(pairs)
        self.assertTrue(
            any(expected_fragment in p for p in problems),
            f"expected problem containing {expected_fragment!r}, got {problems}",
        )

    def test_missing_target(self):
        self.lint([("a", "# A\nsee [x](missing.md)"), ("b", "# B")], "target does not exist")

    def test_bad_internal_link_type(self):
        self.lint([("a", "# A\nsee [y](b.txt)"), ("b", "# B")], "internal link should point at a .md file")

    def test_bad_anchor(self):
        markdown = """
# A

see [x](b.md#nope)
"""
        self.lint([("a", markdown), ("b", "# B\n## real")], "anchor not found")

    def test_duplicate_headings_flagged(self):
        self.lint([("a", "# A\n## x\n## x")], "duplicate heading")

    def test_missing_title_flagged(self):
        self.lint([("a", "no title at all")], "no 'title' first-level heading found")

    def test_card_without_use_line_flagged(self):
        text = "# Cards\n## Card: Broken\n```text\nno For: line\n```"
        self.lint([(pipeline.CARD_STEM, text)], "must be followed by its 'For:' paragraph")

    def test_too_few_cards_flagged(self):
        text = "# Cards\n## Card: One\nFor: only one."
        self.lint([(pipeline.CARD_STEM, text)], "expected at least 4 pattern cards")

    def test_clean_docs_pass(self):
        pairs = [("a", "# A\nsee [glossary](b.md#token)\n\ntext"), ("b", "# B\n\n## token\nbody")]
        self.assertEqual(pipeline.lint_docs(pairs), [])


class BuildTests(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="handbook-build-"))
        self.addCleanup(shutil.rmtree, self.tmp)
        self.docs = self.tmp / "docs"
        self.docs.mkdir()
        (self.docs / "01-alpha.md").write_text(FIXTURE_A, encoding="utf-8")
        (self.docs / "05-pattern-cards.md").write_text(FIXTURE_CARDS, encoding="utf-8")
        (self.docs / "09-glossary.md").write_text(FIXTURE_B, encoding="utf-8")
        self.out = self.tmp / "site"

    def test_build_creates_expected_files(self):
        written = pipeline.build_site(self.docs, self.out)
        names = sorted(p.name for p in written)
        self.assertEqual(
            names,
            sorted(
                [
                    "alpha.html",
                    "pattern-cards.html",
                    "cards.html",
                    "glossary.html",
                    "index.html",
                    "book.html",
                    "style.css",
                ]
            ),
        )
        for name in names:
            self.assertTrue((self.out / name).is_file())

    def test_index_has_toc_with_titles(self):
        pipeline.build_site(self.docs, self.out)
        index = (self.out / "index.html").read_text(encoding="utf-8")
        self.assertIn("Glossary Thing", index)
        self.assertIn('href="glossary.html"', index)
        self.assertIn(pipeline.BOOK_TITLE, index)
        self.assertIn('href="cards.html"', index)

    def test_cards_page_lists_every_card(self):
        pipeline.build_site(self.docs, self.out)
        cards_page = (self.out / "cards.html").read_text(encoding="utf-8")
        self.assertIn('id="pc-card-the-alpha-card"', cards_page)
        self.assertIn('href="pattern-cards.html#card-the-beta-card"', cards_page)
        self.assertIn("For: doing alpha things", cards_page)
        self.assertIn("Twelve fill-in-the-blank", cards_page)

    def test_card_anchor_exists_on_chapter_page(self):
        pipeline.build_site(self.docs, self.out)
        chapter = (self.out / "pattern-cards.html").read_text(encoding="utf-8")
        self.assertIn('<h2 id="card-the-alpha-card">', chapter)

    def test_chapter_page_has_nav_pager_meta(self):
        pipeline.build_site(self.docs, self.out)
        alpha = (self.out / "alpha.html").read_text(encoding="utf-8")
        self.assertIn('class="pager"', alpha)
        self.assertIn("Chapter 1 of 3", alpha)
        self.assertIn("<aside>", alpha)
        self.assertIn('name="description"', alpha)
        self.assertIn("<table>", alpha)

    def test_book_build_shows_all_sections(self):
        pipeline.build_site(self.docs, self.out)
        book = (self.out / "book.html").read_text(encoding="utf-8")
        self.assertIn('id="ch-1"', book)
        self.assertIn('id="ch-2"', book)
        self.assertIn('<h1 id="alpha-chapter">', book)
        self.assertIn('href="#ch-2"', book)

    def test_anchor_link_in_doc_points_to_existing_heading(self):
        pipeline.build_site(self.docs, self.out)
        alpha = (self.out / "alpha.html").read_text(encoding="utf-8")
        self.assertIn('href="glossary.html#token-plus"', alpha)
        gloss = (self.out / "glossary.html").read_text(encoding="utf-8")
        self.assertIn('id="token-plus"', gloss)

    def test_site_is_offline(self):
        pipeline.build_site(self.docs, self.out)
        for page in self.out.glob("*.html"):
            text = page.read_text(encoding="utf-8")
            for match in re.finditer(r'(src|href)="(http[^"]+)"', text):
                self.assertTrue(
                    pipeline.AUTHOR_SITE in match.group(2),
                    f"unexpected external reference in {page.name}: {match.group(2)}",
                )

    def test_build_refuses_dangerous_out(self):
        with self.assertRaises(ValueError):
            pipeline.build_site(self.docs, self.docs)
        self.assertEqual(len(list(self.docs.glob("*.md"))), 3)

    def test_lint_failure_blocks_build(self):
        (self.docs / "02-bad.md").write_text("# Bad\n[missing](nowhere.md)\n", encoding="utf-8")
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            with self.assertRaises(SystemExit):
                pipeline.build_site(self.docs, self.out / "elsewhere")
        self.assertIn("DOC LINT", stderr.getvalue())

    def test_missing_title_blocks_build(self):
        (self.docs / "03-notitle.md").write_text("just text, no heading\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            pipeline.build_site(self.docs, self.out / "elsewhere2")


class RepoDocsTests(unittest.TestCase):

    def test_repo_docs_lint_clean(self):
        docs_dir = Path(__file__).resolve().parent.parent / "docs"
        files = sorted(p for p in docs_dir.glob("*.md") if not p.name.startswith("_"))
        docs = [(p.stem, p.read_text(encoding="utf-8")) for p in files]
        self.assertEqual(docs_dir.name, "docs")
        self.assertEqual(len(files), 11, "expected the 11 planned chapters")
        self.assertEqual(pipeline.lint_docs(docs), [])

    def test_repo_build_is_reproducible(self):
        root = Path(__file__).resolve().parent.parent
        docs_dir = root / "docs"
        seen = []
        for run in range(2):
            with tempfile.TemporaryDirectory(prefix="handbook-ci-") as t:
                out = Path(t) / "site"
                pipeline.build_site(docs_dir, out)
                seen.append(sorted((p.name, p.stat().st_size) for p in out.iterdir()))
        self.assertEqual(seen[0], seen[1])

    def test_repo_chapter_cross_references_resolve(self):
        root = Path(__file__).resolve().parent.parent
        docs_dir = root / "docs"
        expected = {
            "00-introduction",
            "01-why-prompts-fail",
            "02-role-context-format",
            "03-iterating-like-an-editor",
            "04-few-shot-examples",
            "05-pattern-cards",
            "06-before-and-after",
            "07-building-a-prompt-library",
            "08-testing-safely",
            "09-glossary",
            "10-cheat-sheet",
        }
        stems = {p.stem for p in docs_dir.glob("*.md")}
        self.assertEqual(stems, expected)
        # every "Chapter N" mention in chapter text must match an existing file
        for p in sorted(docs_dir.glob("*.md")):
            text = p.read_text(encoding="utf-8")
            for number in re.findall(r"Chapter (\d+)", text):
                target = f"{int(number):02d}-"
                self.assertTrue(
                    any(s.startswith(target) for s in stems),
                    f"{p.name} mentions Chapter {number}, but no file {target}* exists",
                )


class CliTests(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="handbook-cli-"))
        self.addCleanup(shutil.rmtree, self.tmp)
        self.docs = self.tmp / "docs"
        self.docs.mkdir()
        (self.docs / "01-alpha.md").write_text(FIXTURE_A, encoding="utf-8")
        (self.docs / "05-pattern-cards.md").write_text(FIXTURE_CARDS, encoding="utf-8")
        (self.docs / "09-glossary.md").write_text(FIXTURE_B, encoding="utf-8")

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "pipeline.py"), *args],
            capture_output=True,
            text=True,
        )

    def test_cli_builds_and_reports(self):
        out = self.tmp / "out"
        result = self.run_cli("--docs", str(self.docs), "--out", str(out))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Built", result.stdout)
        self.assertTrue((out / "index.html").is_file())
        self.assertTrue((out / "book.html").is_file())
        self.assertTrue((out / "cards.html").is_file())

    def test_cli_check_clean_returns_zero(self):
        result = self.run_cli("--check", "--docs", str(self.docs))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("clean", result.stdout)

    def test_cli_check_failure_returns_one(self):
        (self.docs / "02-bad.md").write_text("# Bad\n[missing](gone.md)\n", encoding="utf-8")
        result = self.run_cli("--check", "--docs", str(self.docs))
        self.assertEqual(result.returncode, 1)
        self.assertIn("DOC LINT", result.stderr)

    def test_cli_from_md_prints_html(self):
        result = self.run_cli("--from-md", str(self.docs / "01-alpha.md"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('<h1 id="alpha-chapter">', result.stdout)
        self.assertIn("<table>", result.stdout)

    def test_cli_cards_flag_lists_cards(self):
        result = self.run_cli("--cards", "--docs", str(self.docs))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Card: The Alpha Card", result.stdout)
        self.assertIn("#card-the-beta-card", result.stdout)


SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"gh[p bou]_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)api[_-]?key\s*[=:]\s*['\"][^'\"]{8,}"),
    re.compile(r"(?i)(secret|token)\s*[=:]\s*['\"][^'\"]{16,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]

LICENSE_LINE = "Copyright (c) 2026 Asdale Dynamics, LLC"


class RepoHygieneTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parent.parent
        cls.scanned = [
            p
            for p in cls.root.rglob("*")
            if p.is_file()
            and "site" not in p.parts
            and ".git" not in p.parts
            and "__pycache__" not in p.parts
        ]

    def test_no_secrets_anywhere(self):
        for path in self.scanned:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in SECRET_PATTERNS:
                self.assertIsNone(
                    pattern.search(text),
                    f"possible secret pattern {pattern.pattern} in {path}",
                )

    def test_license_file_exact_copyright(self):
        text = (self.root / "LICENSE").read_text(encoding="utf-8")
        self.assertIn(LICENSE_LINE, text)
        self.assertIn("Permission is hereby granted, free of charge", text)

    def test_readme_credits_the_llc(self):
        text = (self.root / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", text)
        self.assertIn(LICENSE_LINE, text)

    def test_docs_mention_no_keys_or_accounts(self):
        docs = (self.root / "docs").glob("*.md")
        for path in docs:
            text = path.read_text(encoding="utf-8").lower()
            for phrase in ("enter your api key", "subscription required", "sign up for an account"):
                self.assertNotIn(phrase, text, f"{path.name} says {phrase!r}")

    def test_repo_has_no_unexpected_top_level_files(self):
        allowed = {
            "README.md",
            "LICENSE",
            "STATUS.md",
            ".gitignore",
            ".git",
            ".github",
            "scripts",
            "docs",
            "tests",
            "site",
        }
        extra = {p.name for p in self.root.iterdir()} - allowed
        self.assertEqual(extra, set(), f"unexpected files in repo root: {extra}")


if __name__ == "__main__":
    unittest.main()
