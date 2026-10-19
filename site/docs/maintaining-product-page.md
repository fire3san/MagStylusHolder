# Maintaining the product page

The root `index.html`, `css/` and `js/` are the canonical frontend sources.
GitHub Pages currently publishes the repository root. `site/` is a portable
mirror; do not edit its frontend files independently.

## What to edit

| Change | Source |
| --- | --- |
| Page copy, section order, product cards, FAQ answers | `index.html` |
| Theme colors, fonts, navigation, footer | `css/base.css` |
| Visitor introduction, model chooser, first-print guide | `css/discovery.css` |
| Hero image, studio/3D tabs, materials and CAD controls | `css/hero.css` |
| Section layouts, collection cards, story, fit calculator, anatomy, timeline, downloads | `css/sections.css` |
| Drafting, lab notes, lifestyle cards, FAQ | `css/galleries.css` |
| Full-screen image preview | `css/lightbox.css` |
| Model specifications, STL paths, viewer profiles | `js/models.js` |
| Language switching, calculator, gallery interactions | `js/main.js` |
| Three.js viewer behavior | `js/viewer.js` |

`css/style.css` is the public stylesheet entry point. Its import order is
intentional. Component files keep their responsive rules alongside their styles.
Search for a class or section ID before adding a rule; edit the existing component
rather than appending an override to the entry point. Use the theme variables in
`base.css` for shared colors. Preserve more specific surface colors where needed.

The page stays plain HTML/CSS/JavaScript with no build step. Section comments in
`index.html` mark the major editing boundaries. Keep inline text and elements
(such as a heading's `small` label) together when whitespace affects rendering.
Keep presentation in CSS rather than `style` attributes.

## Content and interaction contracts

Preserve IDs and `data-*` attributes used by the scripts, including `data-inspect`,
`data-gallery`, `data-mat` and `data-view`. Keep product cards as static HTML so
content remains readable without JavaScript. A new product also needs a matching
catalog entry in `js/models.js`; its `data-inspect` value must match the catalog key.

Some English/Chinese copy is separately maintained in `js/main.js`. When changing
translated copy, update the corresponding language-switching text there too.
This refactor retains that existing behavior.

## Sync and preview

After editing root frontend files:

```sh
python3 scripts/sync-site.py
python3 scripts/sync-site.py --check
python3 -m http.server 8765 --bind 127.0.0.1
```

Preview both `/` and `/site/` at desktop and phone widths. Check the language
switch, studio/3D tabs, model selection, material/camera controls, fit calculator,
FAQ expansion and gallery opening/closing. Confirm local images and downloads
resolve. The sync command copies HTML, CSS, JavaScript, documentation and README; assets are not
copied automatically, so add new assets to both trees when keeping a portable mirror.
