"""Package the current six print models and refresh output/latest/."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(ROOT / 'scripts/build-print-orientation.py')],
               check=True, stdout=subprocess.DEVNULL)
PACK = ROOT / 'assets/downloads/Selected_6_Holders_Latest'
MODELS = [
    ('AURA_SCREEN_v4_BED_DOWN.stl', 'assets/downloads/print-ready/AURA_SCREEN_v4_BED_DOWN.stl'),
    ('NEXUS_SCREEN_v2_BED_DOWN.stl', 'assets/downloads/print-ready/NEXUS_SCREEN_v2_BED_DOWN.stl'),
    ('AERIS.stl', 'assets/downloads/Tapered_Seats_20261103/AERIS_v10.stl'),
    ('ECLIPSE.stl', 'assets/stl/v9/KM_Arc_BOOX_vertical.stl'),
    ('AXIS.stl', 'assets/stl/side/03_Apple_Pencil_Original_5x1_NoText_PROVISIONAL.stl'),
    ('ORBIT.stl', 'assets/stl/open_spine/A_Open_Spine_Compact.stl'),
]
PACK.mkdir(parents=True, exist_ok=True)
# Remove the superseded screen file from these generated current-only copies.
(PACK / 'AURA_SCREEN_v3.stl').unlink(missing_ok=True)
(ROOT / 'output/latest/selected-six/AURA_SCREEN_v3.stl').unlink(missing_ok=True)
(PACK / 'AURA_SCREEN_v4.stl').unlink(missing_ok=True)
(ROOT / 'output/latest/selected-six/AURA_SCREEN_v4.stl').unlink(missing_ok=True)
for folder in [PACK, ROOT / 'output/latest/selected-six', ROOT / 'site/assets/downloads/Selected_6_Holders_Latest']:
    (folder / 'NEXUS_SCREEN_v2_flat.stl').unlink(missing_ok=True)
for obsolete in ['AURA_SCREEN_v3.stl', 'AURA_SCREEN_v4.stl']:
    (ROOT / 'site/assets/downloads/Selected_6_Holders_Latest' / obsolete).unlink(missing_ok=True)
manifest = []
for filename, source in MODELS:
    shutil.copy2(ROOT / source, PACK / filename)
    manifest.append(dict(file=filename, source=source,
                         sha256=hashlib.sha256((PACK / filename).read_bytes()).hexdigest()))
(PACK / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
(PACK / 'README.md').write_text('''# Latest six print models / 最新六款列印模型

AURA SCREEN v4: retains the 10 mm shortening and 2 mm inward move, with a
supported tapered inner seat, more than 1.5 mm modeled nib clearance and at
least 1.5 mm material around the new seat. Dimensions: 103.50 × 104.54 × 14.90 mm.
AURA_SCREEN_v4_BED_DOWN.stl uses the flat-base-down print orientation.
AERIS uses the v10 tapered-seat revision. Pen-tip length is assumed at 10 mm;
physical fit remains to be tested. Full checks are in Tapered_Seats_20261103.

NEXUS SCREEN remains v2 flat, now also supplied in the bed-down orientation; ECLIPSE remains BOOX v9. AXIS and ORBIT retain
their existing geometry. Earlier versioned packs remain available.

Units: mm. Print at original scale. Six main parts only: no magnets, ring,
spacers or fit coupons. Review Tapered_Seats_20261103 for checks and section images.
STL checks do not establish physical fit, strength or retention.

manifest.json records source paths and SHA-256 hashes for every model.
''')
with zipfile.ZipFile(PACK.with_suffix('.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
    for path in sorted(PACK.iterdir()):
        z.write(path, path.name)


latest = ROOT / 'output/latest'
latest.mkdir(parents=True, exist_ok=True)
shutil.copytree(PACK, latest / 'selected-six', dirs_exist_ok=True)
shutil.copytree(ROOT / 'assets/downloads/Print_Feedback_v3', latest / 'aura-screen-v3', dirs_exist_ok=True)
shutil.copy2(PACK.with_suffix('.zip'), latest / PACK.with_suffix('.zip').name)
shutil.copy2(ROOT / 'assets/downloads/Print_Feedback_v3.zip', latest / 'Print_Feedback_v3.zip')
(latest / 'README.md').write_text('''# Current print files

- `selected-six/`: the current six main STL models, README and source hashes.
- `tapered-seats/`: all seven current closed sheaths, wall checks and section images.
- `aura-screen-v3/`: the superseded first screen revision, kept for comparison.
- ZIP files contain the same files for transfer to a slicer or print supplier.

Canonical deliverables live in assets/downloads; this folder is a local mirror.
Rebuild from the repository root:

    .venv/bin/python scripts/build-tapered-seats.py
    .venv/bin/python scripts/build-latest-pack.py

Earlier engineering builds are in ../archive/, grouped by family and version.
''')
for relative in ['assets/downloads/Selected_6_Holders_Latest',
                 'assets/downloads/Print_Feedback_v3']:
    shutil.copytree(ROOT / relative, ROOT / 'site' / relative, dirs_exist_ok=True)
for relative in ['assets/downloads/Selected_6_Holders_Latest.zip',
                 'assets/downloads/Print_Feedback_v3.zip']:
    shutil.copy2(ROOT / relative, ROOT / 'site' / relative)
print('Current six-model pack, product render, site assets and output/latest refreshed.')
