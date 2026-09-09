"""Regenerate publications.html and the Selected Publications block in index.html
from data/publications.json.

Usage (from the repo root):
    python scripts/build.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "publications.json"
PUBS_PAGE = ROOT / "publications.html"
INDEX_PAGE = ROOT / "index.html"
TEMPLATE = ROOT / "scripts" / "publications.template.html"

SECTIONS = [
    ("article", "Peer-reviewed journal articles", "articles"),
    ("chapter", "Chapters, encyclopedia entries and editorials", "chapters"),
    ("working", "Working papers and manuscripts under review", "working-papers"),
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def format_authors(authors: str) -> str:
    """Escape and bold every 'Kreif N' occurrence."""
    out = esc(authors)
    return re.sub(r"Kreif,? N\b", lambda m: f"<b>{m.group(0)}</b>", out)


def render_pub(p: dict) -> str:
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


def build() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    pubs = data["publications"]
    # Newest first within each section, stable for equal years.
    pubs_sorted = sorted(pubs, key=lambda p: -int(p["year"]))

    # --- publications.html -------------------------------------------------
    blocks = []
    for kind, heading, anchor in SECTIONS:
        items = [render_pub(p) for p in pubs_sorted if p["type"] == kind]
        if not items:
            continue
        blocks.append(
            f'<section id="{anchor}">\n'
            f'  <div class="wrap split">\n'
            f'    <div class="side">\n'
            f'      <h2>{esc(heading)}</h2>\n'
            f'      <p class="muted small">{len(items)} items</p>\n'
            f'    </div>\n'
            f'    <ul class="pub-list">\n' + "\n".join(items) + "\n    </ul>\n"
            f"  </div>\n"
            f"</section>"
        )
    page = TEMPLATE.read_text(encoding="utf-8").replace("{{PUBLICATIONS}}", "\n\n".join(blocks))
    page = page.replace("{{COUNT_ARTICLES}}", str(sum(p["type"] == "article" for p in pubs)))
    PUBS_PAGE.write_text(page, encoding="utf-8")

    # --- selected list on index.html --------------------------------------
    selected = [render_pub(p) for p in pubs_sorted if p.get("selected")]
    index = INDEX_PAGE.read_text(encoding="utf-8")
    start, end = "<!-- selected:start -->", "<!-- selected:end -->"
    if start in index and end in index:
        pre, rest = index.split(start, 1)
        _, post = rest.split(end, 1)
        index = pre + start + '\n<ul class="pub-list">\n' + "\n".join(selected) + "\n</ul>\n" + end + post
        INDEX_PAGE.write_text(index, encoding="utf-8")

    print(f"Wrote {PUBS_PAGE.name} ({len(pubs)} publications) and {len(selected)} selected on {INDEX_PAGE.name}")


if __name__ == "__main__":
    build()
