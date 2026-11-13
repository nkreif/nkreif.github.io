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
    ("working", "Preprints and manuscripts under review", "working-papers"),
]

BLOCK_RE = re.compile(
    r"(<!-- pubs:(?P<tag>[\w-]+):(?P<style>full|compact):start -->)(.*?)(<!-- pubs:(?P=tag):(?P=style):end -->)",
    re.S,
)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


TRAINEES: set[str] = set()   # filled from data/publications.json (names of students and postdocs)


def format_authors(authors: str) -> str:
    """Escape, bold 'Kreif N', and mark student or trainee co-authors with a double dagger."""
    out = []
    for n in (a.strip() for a in authors.split(",") if a.strip()):
        if re.fullmatch(r"Kreif,? N", n):
            out.append(f"<b>{esc(n)}</b>")
        elif n in TRAINEES:
            out.append(f'{esc(n)}<sup class="trainee" title="Student or trainee co-author">‡</sup>')
        else:
            out.append(esc(n))
    return ", ".join(out)


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
    takeaway = f'    <p class="takeaway">{esc(p["takeaway"])}</p>\n' if p.get("takeaway") else ""
    buttons = ([("Paper", p["url"])] if p.get("url") and p["type"] != "working" else []) + \
              [(lnk["label"], lnk["url"]) for lnk in p.get("links", [])]
    actions = ""
    if buttons:
        actions = '    <p class="pub-actions">' + " ".join(
            f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(label)}</a>' for label, u in buttons) + "</p>\n"
    topics = f' data-topics="{esc(" ".join(p.get("topics", [])))}"'
    return (
        f'<li class="pub"{topics}>\n'
        f'  <div class="year">{p["year"]}</div>\n'
        "  <div>\n"
        f'    <p class="ptitle">{title_html}</p>\n'
        f'    <p class="authors">{format_authors(p["authors"])}</p>\n'
        f'    <p class="venue">{esc(p["venue"])}{note}</p>\n'
        f"{takeaway}{actions}"
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
        f'<span class="cite">{esc(first_author(p))}, {esc(journal(p))}'
        f'{", " + esc(p["note"]) if p.get("note") else ""}, {p["year"]}</span></li>'
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
    TRAINEES.update(data.get("trainees", []))
    pubs = sorted(data["publications"], key=lambda p: -int(p["year"]))  # newest first, stable

    # --- publications.html -------------------------------------------------
    def section(anchor: str, heading: str, items: list[str], note: str = "") -> str:
        note_html = f'      <p class="side-note">{esc(note)}</p>\n' if note else ""
        return (
            f'<section id="{anchor}">\n'
            f'  <div class="wrap split">\n'
            f'    <div class="side">\n'
            f'      <h2>{esc(heading)}</h2>\n{note_html}'
            f'    </div>\n'
            f'    <ul class="pub-list">\n' + "\n".join(items) + "\n    </ul>\n"
            f"  </div>\n"
            f"</section>"
        )

    # View 1: by type, newest first.
    by_type = [section(anchor, heading, [render_pub(p) for p in pubs if p["type"] == kind])
               for kind, heading, anchor in SECTIONS if any(p["type"] == kind for p in pubs)]
    # View 2: by primary research theme (the same themes as the CV), all types, newest first.
    themes = data.get("topics", {})
    primary = lambda p: (p.get("topics") or [None])[0]
    by_theme = []
    for code, label in themes.items():
        group = [p for p in pubs if primary(p) == code]
        if group:
            n_art = sum(p["type"] == "article" for p in group)
            by_theme.append(section(f"theme-{code}", label, [render_pub(p) for p in group],
                                    f"{n_art} journal article{'s' if n_art != 1 else ''}"))

    used = {t for p in pubs for t in p.get("topics", [])}
    chips = ['<button type="button" class="chip" data-topic="" aria-pressed="true">All</button>'] + [
        f'<button type="button" class="chip" data-topic="{esc(code)}" aria-pressed="false">{esc(label)}</button>'
        for code, label in themes.items() if code in used]
    views = ('<div class="view" data-view="type">\n' + "\n\n".join(by_type) + "\n</div>\n\n"
             '<div class="view" data-view="theme" hidden>\n' + "\n\n".join(by_theme) + "\n</div>")
    page = (TEMPLATE.read_text(encoding="utf-8")
            .replace("{{TOPICS}}", "\n        ".join(chips))
            .replace("{{PUBLICATIONS}}", views))
    PUBS_PAGE.write_text(page, encoding="utf-8")
    print(f"Wrote {PUBS_PAGE.name} ({len(pubs)} publications)")

    # --- marked blocks on other pages -------------------------------------
    for p in PAGES_WITH_BLOCKS:
        if p.exists():
            print(f"Filled {fill_blocks(p, pubs)} block(s) in {p.name}")


if __name__ == "__main__":
    build()
