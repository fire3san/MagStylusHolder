# Latest individual STL models

Each link below opens one current STL file. A ZIP is not required.
The three SCREEN models use flat-base-down files. The other models retain
their existing orientations. Use 100% scale and review the slicer preview.

| Model | Current version | Individual file |
| --- | --- | --- |
| AURA SCREEN | v4 · bed down | [Download STL](../../assets/downloads/print-ready/AURA_SCREEN_v4_BED_DOWN.stl) |
| NEXUS SCREEN | v2 · bed down | [Download STL](../../assets/downloads/print-ready/NEXUS_SCREEN_v2_BED_DOWN.stl) |
| AURA DUO SCREEN | v3 · bed down | [Download STL](../../assets/downloads/print-ready/AURA_DUO_SCREEN_v3_BED_DOWN.stl) |
| AURA DUO | v4 | [Download STL](../../assets/downloads/Tapered_Seats_20261103/AURA_DUO_v4.stl) |
| AERIS | v10 | [Download STL](../../assets/downloads/Tapered_Seats_20261103/AERIS_v10.stl) |
| VERTEX | v10 | [Download STL](../../assets/downloads/Tapered_Seats_20261103/VERTEX_v10.stl) |
| ECLIPSE | v9 | [Download STL](../../assets/stl/v9/KM_Arc_BOOX_vertical.stl) |
| ZEPHYR | v9 | [Download STL](../../assets/stl/v9/KM_Ribbon_BOOX_vertical.stl) |
| AURA | v4 | [Download STL](../../assets/downloads/Tapered_Seats_20261103/AURA_v4.stl) |
| NEXUS | v3 | [Download STL](../../assets/stl/side/02_Side_QuickClip_PROVISIONAL.stl) |
| AXIS | v3 | [Download STL](../../assets/stl/side/03_Apple_Pencil_Original_5x1_NoText_PROVISIONAL.stl) |
| ORBIT | v9 | [Download STL](../../assets/stl/open_spine/A_Open_Spine_Compact.stl) |
| STRATOS | v9 | [Download STL](../../assets/stl/open_spine/B_Rear_Spine_Extended.stl) |
| TITAN PRO | v10 | [Download STL](../../assets/downloads/Tapered_Seats_20261103/TITAN_PRO_v10.stl) |
| ECLIPSE MINI | v9 | [Download STL](../../assets/stl/v9/KM_Arc_iPad_Pencil89.stl) |

The files linked above live in the tracked canonical assets directories.
This index is tracked, so it is visible on GitHub as well as locally.

Locally, `output/latest/stl/` contains a flat copy of all 15 current models,
with file/source hashes in `manifest.json`. Generated copies, images and ZIPs
remain Git-ignored. Older versions are in `output/archive/`.

Refresh the links, index and flat local copies:

    .venv/bin/python scripts/sync-model-downloads.py
    python3 scripts/sync-site.py

Full build: .venv/bin/python scripts/build-latest-pack.py
