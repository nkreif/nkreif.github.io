"""One-off migration: build data/site.json (the website-only layer on top of the CV's
publication data) from the old hand-kept data/publications.json.

Keeps, per CV publication id: the site's sentence-case title, `selected`, research-page
tags, and non-DOI links. Adds topic codes for the publication filter and preprint/software
links. Run once; afterwards edit data/site.json by hand.
"""
import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CV = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT.parent / "cv")

old = json.loads((ROOT / "data/publications.json").read_text(encoding="utf-8"))["publications"]
cv = yaml.safe_load((CV / "data/publications.yaml").read_text(encoding="utf-8"))["publications"]
cv = [p for p in cv if p["type"] in ("article", "chapter", "working", "submitted") and p.get("include", True)]


def words(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).split()


def doi(u):
    m = re.search(r"10\.\d{4,9}/\S+", u or "")
    return m.group(0).lower() if m else None


TOPICS = {
    "cml": "Causal machine learning and policy learning",
    "ci": "Causal inference for comparative effectiveness and HTA",
    "pe": "Health policy evaluation",
    "gh": "Global health and health systems",
    "mh": "Conflict, violence and mental health",
    "heor": "Outcomes research and economic evaluation",
}
ASSIGN = """
hatamyar2026policy cml | yip2026healthcare heor mh | nwogu2026real heor ci | ochoa-moreno2026increasing gh pe
kneitel2026care heor | shah2026exploring cml gh | rodrigues2026factors pe | kalo2026transferability ci
zhang2026causal ci | shah2025policy cml gh | shah2025heterogeneous cml gh | rodrigues2025digitalization pe
paton2026impact cml mh | diaz2025public pe mh | mcguire2025facility gh pe | counts2025psychological mh
mcguire2025care gh pe | zhang2024machine cml ci | glynn2024integrating cml ci | lordemus2024public mh gh
salas-ortiz2024effect mh | rocha2024covid mh | moler-zapata2022effects gh | rodrigues2022reflection ci
padula2022machine cml | aragon2022long pe | rodrigues2022formalising pe | ciminata2022propensity ci
kreif2022heterogeneous cml gh | kreif2022impact mh gh | mcguire2021effect gh | leon-giraldo2021light mh
leon-giraldo2021inequalities mh gh | stacey2021facility gh pe | kreif2021impact gh ci | chi2020next gh
kreif2021exploiting ci | o'neill2020comparison pe | gaughan2019paying pe | deidda2019framework pe ci
diazordaz2020data cml | kreif2017comparative ci | oneill2016causal pe | kreif2016examination pe
kreif2015evaluation ci cml | miners2014related heor | kreif2016treatment ci | kreif2013regression ci
ishak2013overview heor | kreif2013statistical ci | kreif2012methods ci | muszbek2012modelling heor
radice2012treatment ci | calvo2011cost heor | lux2010cost heor | jarbrink2009quality heor | stull2014validation heor
hatamyar2026machine cml | powell-jackson2026difference pe | kreif2021learning ci | shah2021machine cml
kreif2019machine cml | cussens2025fast cml | hatamyar2023machine cml pe | hatamyar2023policy cml
lordemus2026submitted mh gh | nwogucomparative heor ci | bennett2026haematologica ci
"""
topics = {}
for chunk in ASSIGN.replace("\n", "|").split("|"):
    parts = chunk.split()
    if parts:
        topics[parts[0]] = parts[1:]

LINKS = {
    "shah2026exploring": [{"label": "Preprint", "url": "https://arxiv.org/abs/2501.12803"}],
    "kreif2021exploiting": [{"label": "Preprint", "url": "https://arxiv.org/abs/1806.11153"}],
    "cussens2025fast": [{"label": "Software", "url": "https://cran.r-project.org/package=fastpolicytree"}],
    "lordemus2026submitted": [{"label": "Preprint", "url": "https://doi.org/10.2139/ssrn.6773071"}],
}
# Working papers that are now published (their preprint link sits on the article) and duplicates.
HIDE = {"shah2025exploring", "kreif2018evaluation", "kreif2020benefits", "lordemus2026depression"}

entries, unmatched_old = {}, []
used = set()
for o in old:
    od = doi(o.get("url"))
    best = None
    for p in cv:
        if od and p.get("doi") and od == p["doi"].lower():
            best = p
            break
    if best is None:
        scored = sorted(cv, key=lambda p: -SequenceMatcher(None, words(o["title"]), words(p["title"])).ratio())
        if SequenceMatcher(None, words(o["title"]), words(scored[0]["title"])).ratio() > 0.8:
            best = scored[0]
    if best is None or best["id"] in used:
        unmatched_old.append(o["title"])
        continue
    used.add(best["id"])
    e = {"title": o["title"]}
    if o.get("selected"):
        e["selected"] = True
    if o.get("tags"):
        e["tags"] = o["tags"]
    if o.get("url") and not doi(o["url"]) and "arxiv" not in o["url"]:
        e["url"] = o["url"]          # e.g. publisher page for a chapter without a DOI on the site
    entries[best["id"]] = e

for p in cv:
    e = entries.setdefault(p["id"], {})
    e["topics"] = topics.get(p["id"], [])
    if p["id"] in LINKS:
        e["links"] = LINKS[p["id"]]
    if p["id"] in HIDE:
        e["hide"] = True
    if not e["topics"] and not e.get("hide"):
        print("no topic:", p["id"])

site = {
    "_readme": "Website-only details for publications, keyed by the CV publication id (cv/data/publications.yaml). "
               "title: sentence-case title shown on the site; selected: show on the home page; tags: research-page blocks "
               "(home1-3, strand1-5); topics: filter codes on the publications page; takeaway: one plain-language sentence; "
               "links: extra buttons (Preprint, Code, Software, Slides, Policy brief); hide: leave off the site. "
               "Then run: python scripts/sync_from_cv.py && python scripts/build.py",
    "topics": TOPICS,
    "entries": entries,
}
(ROOT / "data/site.json").write_text(json.dumps(site, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(f"{len(entries)} entries; old site entries not matched to the CV: {len(unmatched_old)}")
for t in unmatched_old:
    print("  -", t[:100])
