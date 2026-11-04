# Print outputs

Start with [latest individual STL downloads](latest/README.md). The latest
index is tracked and visible on GitHub; every model links directly to its
current canonical STL in assets/. ZIP bundles are optional.

| Location | Contents |
| --- | --- |
| latest/README.md | Current individual-model download index (tracked) |
| latest/stl/ | Flat local copy of all 15 current STL models (generated) |
| latest/print-ready/ | Three SCREEN models, flat-base-down STL and previews |
| latest/selected-six/ | Current selected six-model print set |
| latest/tapered-seats/ | Seven supported tip-seat revisions and checks |
| archive/axial/v1–v9/ | Earlier axial engineering builds |
| archive/side/v1–v3/ | Earlier side-holder builds |
| archive/open-spine/v1–v3/ | Earlier open-spine builds |

Refresh the local STL copies and individual links:

    .venv/bin/python scripts/sync-model-downloads.py
    python3 scripts/sync-site.py

Full pack/preview rebuild: .venv/bin/python scripts/build-latest-pack.py

Generated STL copies, ZIPs and images under latest/ stay Git-ignored; their
canonical public files are tracked in assets/. The latest README index is
included in Git so GitHub does not appear to contain archives only.
archive/MIGRATION.json records the earlier verified directory moves.
