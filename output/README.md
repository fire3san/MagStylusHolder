# Print outputs

Start in **latest/** for current printable models. The public product page uses
canonical files in assets/; output/latest is a convenient local copy.

| Folder | Contents |
| --- | --- |
| latest/selected-six/ | Current AURA SCREEN v3, NEXUS SCREEN v2, AERIS, ECLIPSE, AXIS, ORBIT |
| latest/aura-screen-v3/ | AURA SCREEN v3 STL, mesh checks and before/after images |
| archive/axial/v1–v9/ | Earlier axial builds, source, STL, renders and historical guides |
| archive/side/v1–v3/ | Earlier side-holder builds and reviews |
| archive/open-spine/v1–v3/ | Open-spine builds, source and print guides |

Historical folders retain their source/STL/render layout. Do not mix magnet
spacers across versions. archive/MIGRATION.json maps the old paths to new ones;
all moved files were checked by SHA-256 before updating documented paths.

Refresh current models from the repository root:

    .venv/bin/python scripts/build-print-feedback.py
    .venv/bin/python scripts/build-latest-pack.py

latest/ is generated and git-ignored. Previously tracked engineering versions remain
in archive/axial/v1–v7; later local builds remain local. Public downloads live in
assets/downloads/.
