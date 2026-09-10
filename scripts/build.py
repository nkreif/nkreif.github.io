"""Regenerate publications.html, and fill the marked publication blocks in
index.html and research.html, from data/publications.json.

Usage (from the repo root):
    python scripts/build.py

Marked blocks look like
    <!-- pubs:TAG:full:start -->  ...  <!-- pubs:TAG:full:end -->
where TAG is `selected` or any value used in a publication's `tags` list,
and the style is `full` (authors, title, venue) or `compact` (title, then
first author et al., journal, year).
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "publications.json"
PUBS_PAGE = ROOT / "publications.html"
TEMPLATE = ROOT / "scripts" / "publications.template.html"
PAGES_WITH_BLOCKS = [ROOT / "index.html", ROOT / "research.html"]

SECTIONS = [
    ("article", "Peer-reviewed journal articles", "articles"),
    ("chapter", "Chapters, encyclopedia entries and editorials", "chapters"),
    ("working", "Working papers and manuscripts under review", "working-papers"),
]

BLOCK_RE = re.compile(
    r"(<!-- pubs:(?P<tag>[\w-]+):(?P<style>full|compact):start -->)(.*?)(<!-- pubs:(?P=tag):(?P=style):end -->)",
    re.S,
)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def format_authors(authors: str) -> str:
    """Escape and bold every 'Kreif N' occurrence."""
    out = esc(authors)
    return re.sub(r"Kreif,? N\b", lambda m: f"<b>{m.group(0)}</b>", out)


def link(p: dict) -> str:
    return esc(p["url"]) if p.get("url") else "publications.html"


def journal(p: dict) -> str:
    """Journal name without volume and pages."""
    return p["venue"].split(",")[0]


def first_author(p: dict) -> str:
    names = [a.strip() for a in p["authors"].split(",") if a.strip()]
    if not names:
        return ""
    return names[0] if len(names) == 1 else f"{names[0]} et al."


def render_pub(p: dict) -> str:
    """Entry for the publications page and the Selected list."""
    title = esc(p["title"])
    if p.get("url"):
        title_html = f'<a href="{esc(p["url"])}" target="_blank" rel="noopener">{title}</a>'
    else:
        title_html = title
    note = f' <span class="tag">{esc(p["note"])}</span>' if p.get("note") else ""
    return (
        '<li class="pub">\n'
        f'  <div class="year">{p["year"]}</div>\n'
        "  <div>\n"
        f'    <p class="ptitle">{title_html}</p>\n'
        f'    <p class="authors">{format_authors(p["authors"])}</p>\n'
        f'    <p class="venue">{esc(p["venue"])}{note}</p>\n'
        "  </div>\n"
        "</li>"
    )


def render_full(p: dict) -> str:
    """One-line citation with the full author list; title links to the paper."""
    return (
        f'<li>{format_authors(p["authors"])} ({p["year"]}). '
        f'<a href="{link(p)}" target="_blank" rel="noopener">{esc(p["title"])}</a>. '
        f'<i>{esc(p["venue"])}</i>.</li>'
    )


def render_compact(p: dict) -> str:
    """Title, then first author et al., journal and year."""
    return (
        f'<li><a href="{link(p)}" target="_blank" rel="noopener">{esc(p["title"])}</a>'
        f'<span class="cite">{esc(first_author(p))}, {esc(journal(p))}, {p["year"]}</span></li>'
    )


def fill_blocks(page: Path, pubs: list[dict]) -> int:
    text = page.read_text(encoding="utf-8")

    def repl(m: re.Match) -> str:
        tag, style = m.group("tag"), m.group("style")
        if tag == "selected":
            items = [p for p in pubs if p.get("selected")]
            body = '\n<ul class="pub-list">\n' + "\n".join(render_pub(p) for p in items) + "\n</ul>\n"
        else:
            items = [p for p in pubs if tag in p.get("tags", [])]
            render = render_full if style == "full" else render_compact
            cls = "cite-list" if style == "full" else "examples"
            body = f'\n<ul class="{cls}">\n' + "\n".join(render(p) for p in items) + "\n</ul>\n"
        return m.group(1) + body + m.group(5)

    new_text, n = BLOCK_RE.subn(repl, text)
    if n:
        page.write_text(new_text, encoding="utf-8")
    return n


def build() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    pubs = sorted(data["publications"], key=lambda p: -int(p["year"]))  # newest first, stable

    # --- publications.html -------------------------------------------------
    blocks = []
    for kind, heading, anchor in SECTIONS:
        items = [render_pub(p) for p in pubs if p["type"] == kind]
        if not items:
            continue
        blocks.append(
            f'<section id="{anchor}">\n'
            f'  <div class="wrap split">\n'
            f'    <div class="side">\n'
            f'      <h2>{esc(heading)}</h2>\n'
            f'    </div>\n'
            f'    <ul class="pub-list">\n' + "\n".join(items) + "\n    </ul>\n"
            f"  </div>\n"
            f"</section>"
        )
    page = TEMPLATE.read_text(encoding="utf-8").replace("{{PUBLICATIONS}}", "\n\n".join(blocks))
    PUBS_PAGE.write_text(page, encoding="utf-8")
    print(f"Wrote {PUBS_PAGE.name} ({len(pubs)} publications)")

    # --- marked blocks on other pages -------------------------------------
    for p in PAGES_WITH_BLOCKS:
        if p.exists():
            print(f"Filled {fill_blocks(p, pubs)} block(s) in {p.name}")


if __name__ == "__main__":
    build()
