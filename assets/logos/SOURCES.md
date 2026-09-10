# Logo sources

Collected 2026-09-09 for the "affiliations" strip. All marks are trademarks of the
respective institutions and are used here only to indicate affiliation (past or
present); they are not endorsements. Check each institution's brand rules before
recolouring, cropping or placing on coloured backgrounds.

| File | Institution | Format / size | Origin |
|---|---|---|---|
| `uw.svg` | University of Washington | SVG, viewBox 512 x 40 | Wikimedia Commons |
| `york.svg` | University of York | SVG, viewBox 400 x 156 | york.ac.uk site asset (recoloured, see note) |
| `lshtm.svg` | London School of Hygiene & Tropical Medicine | SVG, viewBox 546 x 262 | English Wikipedia (fair-use file) |
| `ceu.svg` | Central European University | SVG, viewBox 180 x 82 | ceu.edu site asset (recoloured, see note) |
| `ceu.png` | Central European University | PNG, 3000 x 1274 | Wikimedia Commons (colour alternative) |
| `corvinus.svg` | Corvinus University of Budapest | SVG, viewBox 561 x 192 | Official logo pack (PDF vector converted to SVG) |
| `berkeley.svg` | University of California, Berkeley | SVG, 225 x 42 | berkeley.edu site asset |
| `kaiser.svg` | Kaiser Permanente Division of Research | SVG, viewBox 300 x 69 | divisionofresearch.kaiserpermanente.org site asset |

## 1. University of Washington -- `uw.svg`

- Source: https://commons.wikimedia.org/wiki/File:University_of_Washington_Purple_left-aligned_signature.svg
  (original file: https://upload.wikimedia.org/wikipedia/commons/9/98/University_of_Washington_Purple_left-aligned_signature.svg)
- Licence line on Commons: "Public domain -- This logo image consists only of simple geometric shapes or text. It does not meet the threshold of originality needed for copyright protection... Trademarked: this work includes material that may be protected as a trademark."
- Brand page: https://www.washington.edu/brand/graphic-elements/logo/ -- the page offers the same "University signature, left-aligned, purple" as PNG and EPS (no SVG). Usage note there: "The block W Logo, University wordmark and combined signature systems are the only sanctioned marks for use... to represent the University of Washington"; logos may appear only in the official colour palette. Questions: uwbrand@uw.edu.
- Note: a School of Pharmacy / CHOICE Institute lock-up was not sourced; the university-level signature is used.

## 2. University of York -- `york.svg`

- Source: https://www.york.ac.uk/static/2/images/uoy_logo_white.svg (the logo file served in the header of york.ac.uk and of the Centre for Health Economics site, https://www.york.ac.uk/che/).
- Modification: the original is the white "reversed" version (`path{fill:white}`); the single style rule was changed to `fill:#000000` to give the standard single-colour black logo, and the mis-cased `viewbox` attribute was corrected to `viewBox`. Nothing else was altered.
- Licence / usage note: no licence is shown with the asset; it is the University's trademarked logo. The public brand page https://www.york.ac.uk/staff/external-relations/brand/ states that logo downloads are available from the University of York Brand Platform (https://brand.york.ac.uk/), which requires a University login ("you need to log in to download the University logo"). The guidelines PDF is public at https://brand.york.ac.uk/guidelines/guide/3aa7d642-ac22-4c14-b3a8-778a8d1ded27/page/35296c4d-cbec-43d4-85a2-84f211f43219 .
- Brand page: https://www.york.ac.uk/staff/external-relations/brand/ (logo page itself https://www.york.ac.uk/staff/external-relations/brand/logo/ returns 401 without login).
- Alternative on Wikipedia (not used, lower quality): https://en.wikipedia.org/wiki/File:UoY_logo_with_shield_2016.png (435 x 171, fair use).

## 3. London School of Hygiene & Tropical Medicine -- `lshtm.svg`

- Source: https://en.wikipedia.org/wiki/File:London_School_of_Hygiene_and_Tropical_Medicine_logo.svg
  (original file: https://upload.wikimedia.org/wikipedia/en/b/bb/London_School_of_Hygiene_and_Tropical_Medicine_logo.svg)
- Licence line on the file page: "Fair use of copyrighted material in the context of London School of Hygiene & Tropical Medicine" (non-free logo; credited to https://www.lshtm.ac.uk/research/centres/centre-history-public-health).
- Brand page: none publicly reachable. https://www.lshtm.ac.uk/aboutus/introducing/brand returns 403 (Cloudflare challenge) from a script; the LSHTM site itself does not expose a standalone logo file (the header logo is an icon-font glyph). Wikimedia Commons only has the seal (https://commons.wikimedia.org/wiki/File:LSHTM.Logo.png, CC BY-SA 4.0), not the wordmark.
- Note: this is the full black wordmark + seal, the standard LSHTM logo; it is the only vector version found outside LSHTM's internal brand site.

## 4. Central European University -- `ceu.svg` and `ceu.png`

- `ceu.svg` source: https://www.ceu.edu/themes/custom/nador/logo_v2.svg (the current CEU logo as served in the ceu.edu site header; 3 paths: "Triangles", "CEU", "Central_European_University").
- Modification: the original is the white reversed version (`fill:#fff`); the fill was changed to `#1e1e1e` (the near-black used in the colour logo) to give a single-colour positive version. Geometry unchanged.
- `ceu.png` source: https://commons.wikimedia.org/wiki/File:Central_European_University_logo.png
  (original file: https://upload.wikimedia.org/wikipedia/commons/4/42/Central_European_University_logo.png, 3000 x 1274). Licence line on Commons: "Public domain" (uploader's own work; textlogo). This is the two-colour version (near-black with cyan #0098c3 accent triangles) and is kept as the colour alternative.
- Licence / usage note: trademark of Central European University; no public licence statement on ceu.edu. CEU's logo files and Graphics Standards Guide are distributed internally by the Communications, Marketing & Outreach Office (https://www.ceu.edu/unit/communications-marketing-outreach-office); no public brand/press-kit page was found.
- Not used: https://commons.wikimedia.org/wiki/File:Central_European_University_Logo.svg (public domain) -- this is the pre-2016 serif logo, superseded.

## 5. Corvinus University of Budapest -- `corvinus.svg`

- Source: official logo pack "Corvinus University of Budapest" (English version) from the Corvinus "Design elements" page:
  https://www.uni-corvinus.hu/downloads/aj08.iay5z6/corvinus-university-of-budapest.zip
  -> `Print Quality Vector/corvinus_University_logo_black.pdf`. The single-page PDF vector was converted to SVG with PyMuPDF (`page.get_svg_image`) and the viewBox cropped to the artwork bounds (the PDF page has large empty margins). The pack also contains AI/EPS vectors and 919 x 554 PNG/JPG office versions in black and white.
- Brand page: https://www.uni-corvinus.hu/ind/design-elements/?lang=en (design guidelines PDF: https://www.uni-corvinus.hu/downloads/aj00.1fej3x3/corvinus-university-design-guidelines.pdf).
- Licence / usage note on the page: no explicit licence; the page distributes the university's official brand materials ("The Corvinus University provides new branding materials... welcome feedback if you notice any issues"). Trademark of Corvinus University of Budapest.
- Alternative (not used): https://www.uni-corvinus.hu/contents/themes/corvinus-theme/library/img/corvinus_logo_2024_en.svg (site header SVG, identical design).

## 6. University of California, Berkeley -- `berkeley.svg`

- Source: https://www.berkeley.edu/wp-content/themes/berkeleygateway/img/logo-berkeley.svg (the current "UC Berkeley" wordmark as served in the berkeley.edu site header; fill #002676 = Berkeley Blue). Only change: added `viewBox="0 0 225 42"` (the original has width/height only) so it scales in CSS.
- Brand page: https://brand.berkeley.edu/identity-resources/logos/ ; downloads (login not required for the page, but the toolkit files are not linked directly): https://brand.berkeley.edu/downloads/brand-essentials-toolkit/
- Usage note on the brand page: "The UC Berkeley logo serves as the campus' primary logo and trademark... The UC Berkeley logo should never be recreated or typeset. Only official logo files should be used in communications."
- Not used: https://commons.wikimedia.org/wiki/File:University_of_California,_Berkeley_logo.svg (public domain) -- the pre-2024 "Berkeley / University of California" logo, superseded.

## 7. Kaiser Permanente Division of Research -- `kaiser.svg`

- Source: https://divisionofresearch.kaiserpermanente.org/wp-content/uploads/2022/11/logo-mobile.svg (stacked "Kaiser Permanente | Division of Research" lock-up served on the Division of Research site; fill #006ba6). Unmodified.
- Horizontal variant (not saved): https://divisionofresearch.kaiserpermanente.org/wp-content/uploads/2022/11/logo02.svg (606 x 31).
- Licence / usage note: no licence shown; registered trademark of Kaiser Foundation Health Plan, Inc. Kaiser Permanente does not publish a public brand/press-kit page; media enquiries via https://about.kaiserpermanente.org/ .
- Plain Kaiser Permanente logo (not used, but available): https://commons.wikimedia.org/wiki/File:KP_logo.svg (public domain, textlogo; 512 x 58).
