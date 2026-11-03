# Print files and engineering outputs

Use `assets/downloads/Selected_6_Holders_Latest.zip` for the current six main
models. It includes AURA SCREEN v4, NEXUS SCREEN v2 flat, AERIS BOOX v10,
ECLIPSE BOOX v9, AXIS and ORBIT. Its manifest records canonical source paths
and SHA-256 hashes. Earlier public download URLs remain available.

`output/` is grouped by purpose, then model family and version:

```text
output/
├── README.md
├── latest/
│   ├── selected-six/        # Current six STL files + source manifest
│   ├── tapered-seats/      # STL, checks, comparisons and internal section
│   └── *.zip               # Matching transfer packs
└── archive/
    ├── axial/v1–v9/        # Original axial prototypes and subsequent versions
    ├── side/v1–v3/         # Side-holder experiments
    ├── open-spine/v1–v3/   # Open-spine experiments
    └── MIGRATION.json      # Old-to-new directory map
```

The former loose `output/` files, `source/` and `stl/` belong to the original
axial prototype and now live together in `archive/axial/v1/`. Old `output/vN/`
directories moved to `archive/axial/vN/`. Side and open-spine versions retain
their source, STL, render, review and guide files in each version folder.
All 384 moved files were checked by SHA-256 before updating documented paths.
Previously tracked histories remain trackable; generated latest files and
previously local later builds remain ignored by Git.

Refresh the current deliverables from the repository root:

```sh
.venv/bin/python scripts/build-tapered-seats.py
.venv/bin/python scripts/build-latest-pack.py
python3 scripts/sync-site.py
python3 scripts/sync-site.py --check
```

`build-latest-pack.py` copies the current canonical files into `output/latest/`
and the portable `site/` asset mirror. Edit model generators or canonical
assets, then rebuild; do not edit the generated latest copies independently.

The product catalog `js/models.js` and static product card both select the
same AURA SCREEN v4 STL. Other models keep their existing revisions. The v3
internal seat assumes a 10 mm pen tip, so physical seating still needs checking.
