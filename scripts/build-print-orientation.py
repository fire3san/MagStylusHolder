"""Make rigidly rotated, bed-down screen products; no model shape changes."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import zipfile

import numpy as np
import trimesh
import manifold3d as mf
from PIL import ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/aura_duo'))
from render_common import render

OUT = ROOT / 'assets/downloads/print-ready'
OUT.mkdir(parents=True, exist_ok=True)
MODELS = [
    ('AURA_SCREEN_v4', 'assets/downloads/Tapered_Seats_20261103/AURA_SCREEN_v4.stl'),
    ('NEXUS_SCREEN_v2', 'assets/stl/screen-facing/NEXUS_SCREEN.stl'),
    ('AURA_DUO_SCREEN_v3', 'assets/downloads/Tapered_Seats_20261103/AURA_DUO_SCREEN_v3.stl'),
]
all_checks = {}
for name, relative in MODELS:
    SOURCE = ROOT / relative
    source = trimesh.load_mesh(SOURCE)
    part = source.copy()
    # Proper 180-degree rotation around X, not a reflection of the geometry.
    transform = np.diag([1., -1., -1., 1.])
    transform[2, 3] = source.bounds[1, 2]
    part.apply_transform(transform)
    path = OUT / f'{name}_BED_DOWN.stl'
    part.export(path)
    part = trimesh.load_mesh(path)
    assert part.is_watertight and part.is_winding_consistent
    s = mf.Manifold(mf.Mesh(np.asarray(part.vertices, np.float32), np.asarray(part.faces, np.uint32)))
    assert s.status() == mf.Error.NoError and len(s.decompose()) == 1
    assert abs(part.volume - source.volume) < .01
    assert np.allclose(part.extents, source.extents, atol=1e-4)
    assert abs(part.bounds[0, 2]) < 1e-5
    bed_faces = np.all(abs(part.triangles[:, :, 2]) < 1e-5, axis=1)
    contact_area = float(part.area_faces[bed_faces].sum())
    assert contact_area > 1000
    assert np.all(part.face_normals[bed_faces, 2] < -.999)
    checks = dict(source=str(SOURCE.relative_to(ROOT)), file=path.name,
                  source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  rotation='180 degrees about X; rigid rotation only',
                  transform_matrix=transform.tolist(), watertight=True, connected_solids=1,
                  bounds_mm=part.bounds.round(5).tolist(), extents_mm=part.extents.round(5).tolist(),
                  planar_bed_contact_area_mm2=round(contact_area, 3),
                  bottom_z_mm=round(float(part.bounds[0, 2]), 7),
                  volume_difference_mm3=round(float(part.volume - source.volume), 7))
    (OUT / f'{name}_orientation.json').write_text(json.dumps(checks, indent=2) + '\n')
    # Render the actual transformed mesh above a build-plate surface.
    center = part.bounds.mean(axis=0)
    center[2] = 0
    plate = trimesh.creation.box((140, 140, .5))
    plate.apply_translation((center[0], center[1], -.25))
    pic = render([(plate.triangles - center, (220, 222, 215)),
                  (part.triangles - center, (42, 100, 101))],
                 w=1000, h=760, scale=4.3, rx=-48, rz=-20)
    draw = ImageDraw.Draw(pic)
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 22)
    draw.text((24, 20), name.replace('_', ' ') + ' / FLAT BASE DOWN / Z = 0', font=font, fill='#20494a')
    draw.text((24, 715), 'Same model. Pen axis horizontal; holder opening upward.', font=font, fill='#20494a')
    pic.save(OUT / f'{name}_BED_DOWN.png')
    render([(part.triangles - part.bounds.mean(axis=0), (42, 100, 101))],
           w=900, h=740, scale=5.2, rx=-48, rz=-20).save(OUT / f'{name}_BED_DOWN_preview.png')
    all_checks[name] = checks

(OUT / 'checks.json').write_text(json.dumps(all_checks, indent=2) + '\n')
(OUT / 'README.md').write_text('# Screen products — flat-base-down print orientation\n\nAURA SCREEN v4, NEXUS SCREEN v2 and AURA DUO SCREEN v3 are supplied as\n*_BED_DOWN.stl. Each is rigidly rotated 180 degrees about X and moved to Z=0.\nNo scaling, mirroring, wall, bore, tip-seat or dimensional changes were made.\n\nThe broad flat backing lies on the build plate; the holder opening faces up.\nThe long pen axis lies horizontally. These are the files selected by the\nproduct page. The original assembly-coordinate files remain available in\nolder packs and source assets.\n\nUse 100% scale and preserve the supplied rotation. Move/center the part on the\nplate as needed. Review the layer preview and support settings separately;\nthis pack does not specify a printer profile or guarantee support-free printing.\n\nchecks.json and the per-model orientation JSON files record the source/output\nhashes, rigid transform, Z bounds, unchanged volume/dimensions and bed contact.\nRebuild: .venv/bin/python scripts/build-print-orientation.py\n')
archive = ROOT / 'assets/downloads/Screen_Products_Bed_Down.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zf:
    for p in sorted(OUT.iterdir()):
        zf.write(p, p.name)
for target in [ROOT / 'site/assets/downloads/print-ready', ROOT / 'output/latest/print-ready']:
    shutil.copytree(OUT, target, dirs_exist_ok=True)
shutil.copy2(archive, ROOT / 'site/assets/downloads' / archive.name)
shutil.copy2(archive, ROOT / 'output/latest' / archive.name)
print(json.dumps(all_checks, indent=2))
