#!/usr/bin/env python3
"""Render Pelori's legal markdown sources into wrapped HTML pages.

Reads from the sibling pelori_app repo:

    pelori_app/docs/privacy.md         -> pelori_website/privacy.html
    pelori_app/docs/terms.md           -> pelori_website/terms.html
    pelori_app/docs/delete_account.md  -> pelori_website/delete-account.html

The renderer supports the markdown subset the three sources actually
use — ATX headings, ordered + unordered lists with indented
continuation lines, blockquotes, paragraphs, inline code, bold,
italic, and links. Anything fancier is not supported on purpose:
keep the sources within this subset.

Output is intentionally deterministic and matches the existing
hand-edited HTML byte-for-byte, so re-running the script after any
markdown edit produces a clean, diff-friendly result.

Usage:
    python3 render_legal.py              # render all three pages
    python3 render_legal.py privacy.md   # render just one
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SITE_ROOT = SCRIPT_DIR.parent
# The two repos live as siblings on disk; the script does not rely on
# any environment variable.
APP_DOCS = SITE_ROOT.parent / "pelori_app" / "docs"

# Stylesheet cache-buster — bump in lockstep with the other site pages
# when styles.css changes materially.
STYLES_VERSION = "20260508"

# source filename -> (output filename, <title> chunk)
PAGES: dict[str, tuple[str, str]] = {
    "privacy.md": ("privacy.html", "Privacy Policy"),
    "terms.md": ("terms.html", "Terms of Service"),
    "delete_account.md": ("delete-account.html", "Delete account"),
}


HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Pelori</title>
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="icon" href="assets/apple-touch-icon.png" type="image/png">
  <link rel="stylesheet" href="styles.css?v={styles_version}">
</head>
<body>
  <header class="nav">
    <div class="container nav-row">
      <a href="/" class="lockup">
        <img src="assets/logos/logo-mark.svg" alt="">
        <span class="lockup-name">pelori</span>
      </a>
      <div class="nav-right">
        <nav class="nav-links">
          <a href="index.html#features" data-i18n="nav.features">Features</a>
          <a href="index.html#beta" data-i18n="nav.beta">Beta</a>
          <a href="faq.html" data-i18n="nav.faq">FAQ</a>
        </nav>
        <div class="lang-picker" id="lang-picker">
          <button type="button" id="lang-btn" class="lang-btn"
                  aria-haspopup="listbox" aria-expanded="false"
                  aria-label="Language">
            <span id="lang-flag" class="lang-flag" aria-hidden="true"></span>
            <span id="lang-name" class="lang-name"></span>
            <svg class="lang-chevron" aria-hidden="true" viewBox="0 0 10 6">
              <path fill="currentColor" d="M0 0l5 6 5-6z"/>
            </svg>
          </button>
          <ul id="lang-menu" class="lang-menu" role="listbox" hidden></ul>
        </div>
        <button type="button" class="nav-burger" id="nav-burger"
                aria-label="Open menu" aria-controls="nav-drawer" aria-expanded="false">
          <svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true">
            <path fill="currentColor" d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/>
          </svg>
        </button>
      </div>
    </div>
    <aside class="nav-drawer" id="nav-drawer" aria-hidden="true">
      <button type="button" class="nav-drawer-close" data-nav-close
              aria-label="Close menu">&times;</button>
      <a href="index.html#features" data-i18n="nav.features" data-nav-close>Features</a>
      <a href="index.html#beta" data-i18n="nav.beta" data-nav-close>Beta</a>
      <a href="faq.html" data-i18n="nav.faq" data-nav-close>FAQ</a>
    </aside>
  </header>
  <main class="legal-body">
    <a href="index.html" class="legal-back" data-i18n="legal.back">&larr; Back to home</a>
    <p class="legal-en-banner" data-legal-en-only data-i18n="legal.en_only" hidden>This page is available in English only — the app itself is fully localised.</p>
    """

FOOT_TEMPLATE = """  </main>
  <footer>
    <div class="container footer-row">
      <span data-i18n="footer.copyright">© 2026 Pelori.</span>
      <div class="footer-links">
        <a href="faq.html" data-i18n="footer.faq">FAQ</a>
        <a href="whats-new.html" data-i18n="footer.whatsNew">What's new</a>
        <a href="privacy.html" data-i18n="footer.privacy">Privacy</a>
        <a href="terms.html" data-i18n="footer.terms">Terms</a>
        <a href="mailto:hello@pelori.fit" data-i18n="footer.contact">Contact</a>
      </div>
    </div>
  </footer>
  <script src="assets/i18n.js"></script>
  <script src="assets/nav-drawer.js"></script>
</body>
</html>
"""


# Sentinel byte sequences used to stash inline-code spans before we
# touch the rest of the inline transforms. Spaces would also work but
# null bytes are cheaper to scan for and can't appear in the source.
_CODE_SENTINEL = "\x00CODE{}\x00"
_LINK_SENTINEL = "\x00LINK{}\x00"


def render_inline(text: str) -> str:
    """Apply inline markdown (code, links, bold, italic) to one chunk
    of text and HTML-escape everything else.

    Order matters: code first (its contents are opaque), then escape,
    then links (so URLs aren't mangled by emphasis matching), then
    bold (`**`) before italic (`*`).
    """
    code_spans: list[str] = []

    def stash_code(m: re.Match[str]) -> str:
        code_spans.append("<code>" + html.escape(m.group(1), quote=False) + "</code>")
        return _CODE_SENTINEL.format(len(code_spans) - 1)

    text = re.sub(r"`([^`]+)`", stash_code, text)

    link_specs: list[str] = []

    def stash_link(m: re.Match[str]) -> str:
        label, url = m.group(1), m.group(2)
        link_specs.append(
            f'<a href="{html.escape(url, quote=True)}">'
            f"{html.escape(label, quote=False)}</a>"
        )
        return _LINK_SENTINEL.format(len(link_specs) - 1)

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", stash_link, text)

    text = html.escape(text, quote=False)

    # Both regexes allow newlines inside the span — markdown sources
    # wrap at ~70 chars so a single *italic* or **bold** routinely
    # straddles a line break. Excluding \n here silently leaves the
    # asterisks in the output.
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", text)

    for i, code in enumerate(code_spans):
        text = text.replace(_CODE_SENTINEL.format(i), code)
    for i, link in enumerate(link_specs):
        text = text.replace(_LINK_SENTINEL.format(i), link)
    return text


_HEADING_RE = re.compile(r"^(#{1,6}) (.+)$")
_OL_RE = re.compile(r"^\d+\. (.*)$")
_BLOCK_PREFIXES = ("- ", "> ", "#")


def _starts_block(line: str) -> bool:
    return (
        line.startswith(_BLOCK_PREFIXES)
        or bool(_OL_RE.match(line))
        or not line.strip()
    )


def render_body(md: str) -> str:
    """Convert a markdown source string into the HTML body fragment
    that sits between the head template and FOOT_TEMPLATE."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        m = _HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            text = render_inline(m.group(2))
            out.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        if line.startswith("- ") or line.startswith("  - "):
            # Flat <ul>. Top-level `- ` bullets and 2-space-indented
            # `  - ` sub-bullets are emitted as siblings inside the
            # same list (matches the existing published HTML — the
            # source uses nesting for readability but the rendered
            # output has always been flat). Continuation lines for
            # either depth are appended as-is so their indent is
            # preserved in the <li>.
            items: list[str] = []
            while i < len(lines):
                curr = lines[i]
                if curr.startswith("  - "):
                    prefix = 4
                elif curr.startswith("- "):
                    prefix = 2
                else:
                    break
                item_lines = [curr[prefix:]]
                i += 1
                while i < len(lines):
                    nxt = lines[i]
                    if not nxt.strip():
                        break
                    if nxt.startswith("- ") or nxt.startswith("  - "):
                        break
                    if nxt.startswith(" "):
                        item_lines.append(nxt)
                        i += 1
                    else:
                        break
                items.append(render_inline("\n".join(item_lines)))
            out.append(
                "<ul>\n"
                + "\n".join(f"<li>{item}</li>" for item in items)
                + "\n</ul>"
            )
            continue

        if _OL_RE.match(line):
            items = []
            while i < len(lines) and _OL_RE.match(lines[i]):
                first = _OL_RE.match(lines[i]).group(1)  # type: ignore[union-attr]
                item_lines = [first]
                i += 1
                # OL continuation: 3-space indent (matches "1. " width).
                while i < len(lines) and lines[i].startswith("   "):
                    item_lines.append(lines[i])
                    i += 1
                items.append(render_inline("\n".join(item_lines)))
            out.append(
                "<ol>\n"
                + "\n".join(f"<li>{item}</li>" for item in items)
                + "\n</ol>"
            )
            continue

        if line.startswith("> "):
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].startswith("> "):
                quote_lines.append(lines[i][2:])
                i += 1
            inner = render_inline("\n".join(quote_lines))
            out.append(f"<blockquote>\n<p>{inner}</p>\n</blockquote>")
            continue

        para_lines: list[str] = []
        while i < len(lines) and not _starts_block(lines[i]):
            para_lines.append(lines[i])
            i += 1
        text = render_inline("\n".join(para_lines))
        out.append(f"<p>{text}</p>")

    return "\n".join(out) + "\n"


def render_page(source: Path, title: str) -> str:
    md = source.read_text(encoding="utf-8")
    head = HEAD_TEMPLATE.format(title=title, styles_version=STYLES_VERSION)
    return head + render_body(md) + FOOT_TEMPLATE


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        targets = {Path(a).name: PAGES[Path(a).name] for a in argv[1:]}
    else:
        targets = PAGES

    for source_name, (output_name, title) in targets.items():
        source = APP_DOCS / source_name
        output = SITE_ROOT / output_name
        if not source.exists():
            print(f"missing source: {source}", file=sys.stderr)
            return 1
        html_out = render_page(source, title)
        output.write_text(html_out, encoding="utf-8")
        print(f"rendered {source.relative_to(SITE_ROOT.parent)} -> "
              f"{output.relative_to(SITE_ROOT.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
