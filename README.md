# nkreif.github.io

Personal academic website of Noémi Kreif, served by GitHub Pages at <https://nkreif.github.io>.

Plain HTML and CSS, no framework and no build tool for the pages themselves.

## Layout

| Path | Purpose |
|---|---|
| `index.html` | Home: bio, research themes, selected publications, recent news, contact |
| `research.html` | The five strands of research, funded projects, collaborators |
| `publications.html` | Generated from `data/publications.json` |
| `assets/style.css` | The one stylesheet (light and dark themes) |
| `assets/Kreif_CV.pdf` | Downloadable CV |
| `data/publications.json` | Generated from the CV repository by `scripts/sync_from_cv.py`; do not edit |
| `data/site.json` | Website-only publication details (titles, selection, tags, takeaways, links) |
| `scripts/sync_from_cv.py` | Builds `data/publications.json` from the CV data plus `data/site.json` |
| `scripts/build.py` | Regenerates `publications.html` and the publication blocks on `index.html` and `research.html` |

## Updating publications

Publications are not edited here. The single source is the CV repository (`../cv`, GitHub `nkreif/cv`):
facts in `cv/data/publications.yaml`, research themes in `cv/data/themes.yaml`, trainee names in
`cv/data/trainees.yaml`.

1. Update the CV data (the `cv-update` skill does this) and rebuild the CV.
2. Website-only details go in `data/site.json`, keyed by the CV publication id: sentence-case title,
   `selected` (home page), research-page `tags` (home1-3, strand1-5), a one-sentence `takeaway`,
   extra `links` (Preprint, Code, Software, Slides, Policy brief), or `hide`.
3. Run `python scripts/sync_from_cv.py` (regenerates `data/publications.json`), then `python scripts/build.py`.
4. Commit and push.

## Updating the CV

Copy the latest PDF from the CV repository (`../cv/build/cv.pdf`) to `assets/Kreif_CV.pdf`. The site has no separate CV page; the CV menu item opens the PDF.

## Local preview

```
python -m http.server 8000
```

then open <http://localhost:8000>.
