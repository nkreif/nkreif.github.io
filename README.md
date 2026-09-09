# nkreif.github.io

Personal academic website of Noémi Kreif, served by GitHub Pages at <https://nkreif.github.io>.

Plain HTML and CSS, no framework and no build tool for the pages themselves.

## Layout

| Path | Purpose |
|---|---|
| `index.html` | Home: bio, research themes, selected publications, recent news, contact |
| `research.html` | The five strands of research, funded projects, collaborators |
| `publications.html` | Generated from `data/publications.json` |
| `cv.html` | Positions, education, teaching, supervision, service, talks |
| `assets/style.css` | The one stylesheet (light and dark themes) |
| `assets/Kreif_CV.pdf` | Downloadable CV |
| `data/publications.json` | Source of truth for publications |
| `scripts/build.py` | Regenerates `publications.html` and the selected list on `index.html` |

## Updating publications

1. Edit `data/publications.json` (add an entry; set `"selected": true` to feature it on the home page).
2. Run `python scripts/build.py`.
3. Commit and push. GitHub Pages redeploys within a minute or two.

## Updating the CV

Replace `assets/Kreif_CV.pdf` and edit `cv.html` by hand.

## Local preview

```
python -m http.server 8000
```

then open <http://localhost:8000>.
