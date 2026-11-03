"""Inspect current catalog STL interiors, including the actual pen-tip envelope.

Run with .venv/bin/python scripts/check-tip-seats.py. No models are modified.
"""
from pathlib import Path
import json
import hashlib
import sys
import shutil

import numpy as np
import trimesh
import manifold3d as mf
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/aura_duo'))
from render_common import render

CATALOG_TEXT = (ROOT / 'js/models.js').read_text()
CATALOG = json.loads(CATALOG_TEXT[CATALOG_TEXT.index('{'):].rstrip().rstrip(';'))
OUT = ROOT / 'assets/reviews/tip-seats'
OUT.mkdir(parents=True, exist_ok=True)
# Coordinates refer to the exported models, not to their centered viewer mesh.
SHEATHS = [
    ('AURA_SCREEN', 'AURA SCREEN v3', -64, -5.2, -68.2, -68.19, 9.0, 157.5),
    ('Side_Scabbard_v3', 'AURA', -60.3, 8.6, -66, -63, 9.0, 157.5),
    ('AURA_DUO_iPhone', 'AURA DUO', -53.55, 8.6, -66, -63, 8.9, 166),
    ('AURA_DUO_SCREEN', 'AURA DUO SCREEN', -53.55, -5.2, -66, -63, 8.9, 166),
    ('S_Flow_BOOX_vertical', 'AERIS', 0, 9.8, -61.96, -58.96, 9.0, 157.5),
    ('S_Facet_BOOX_vertical', 'VERTEX', 0, 9.8, -51.96, -48.96, 9.0, 157.5),
    ('S_Flow_iPad_Pencil89', 'TITAN PRO', 0, 9.8, -82.5, -79.5, 8.9, 166),
]
REVISION_CHECKS = ROOT / 'assets/downloads/Tapered_Seats_20261103/checks.json'
if REVISION_CHECKS.is_file():
    revisions = json.loads(REVISION_CHECKS.read_text())
    updated = []
    for key, name, x, z, floor, tip, diameter, length in SHEATHS:
        if key in revisions:
            d = revisions[key]
            assert CATALOG[key]['path'].endswith(d['file']) or CATALOG[key]['path'].endswith(d['revision'] + '_BED_DOWN.stl')
            name, x, z = d['revision'], d['pen_axis_x_mm'], d['pen_axis_z_mm']
            floor, tip = d['internal_floor_y_mm'], d['modeled_pen_tip_y_mm']
        updated.append((key, name, x, z, floor, tip, diameter, length))
    SHEATHS = updated


def solid(mesh):
    return mf.Manifold(mf.Mesh(np.asarray(mesh.vertices, np.float32),
                               np.asarray(mesh.faces, np.uint32)))


def mesh(s):
    q = s.to_mesh()
    return trimesh.Trimesh(np.asarray(q.vert_properties)[:, :3], np.asarray(q.tri_verts), process=True)


def cylinder(r, length, x, y, z, top_radius=None):
    return (mf.Manifold.cylinder(length, r, r if top_radius is None else top_radius,
                                circular_segments=96)
            .rotate((-90, 0, 0)).translate((x, y, z)))


def first_ray_distance(tris, origin, direction):
    # Moller-Trumbore ray intersections; no optional rtree/scipy dependency.
    direction = np.asarray(direction, float)
    e1, e2 = tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]
    h = np.cross(np.broadcast_to(direction, e2.shape), e2)
    a = np.einsum('ij,ij->i', e1, h)
    good = abs(a) > 1e-10
    f = np.zeros_like(a)
    f[good] = 1 / a[good]
    s = np.asarray(origin) - tris[:, 0]
    u = f * np.einsum('ij,ij->i', s, h)
    q = np.cross(s, e1)
    v = f * (q @ direction)
    t = f * np.einsum('ij,ij->i', e2, q)
    hits = t[good & (u >= -1e-7) & (v >= -1e-7) & (u + v <= 1 + 1e-7) & (t > 1e-7)]
    return None if not len(hits) else float(hits.min())


results = {}
images = []
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 18)
for key, name, x, z, expected_floor, tip_y, pen_d, pen_length in SHEATHS:
    path = ROOT / CATALOG[key]['path']
    part = trimesh.load_mesh(path)
    bed_down = path.name.endswith('_BED_DOWN.stl')
    if bed_down:
        orientation = json.loads((path.parent / (path.stem.removesuffix('_BED_DOWN') + '_orientation.json')).read_text())
        part.apply_transform(np.linalg.inv(np.asarray(orientation['transform_matrix'])))
    s = solid(part)
    assert s.status() == mf.Error.NoError and len(s.decompose()) == 1
    assert part.is_watertight
    floor = tip_y - first_ray_distance(part.triangles, [x, tip_y, z], [0, -1, 0])
    assert abs(floor - expected_floor) < .001, (key, floor)
    radii = [first_ray_distance(part.triangles, [x, floor + d, z], [1, 0, 0])
             for d in [.5, 2, 4]]
    tapered = max(radii) - min(radii) > .2
    pen_tip = cylinder(.1, 10, x, tip_y, z, pen_d / 2)
    barrel = cylinder(pen_d / 2, pen_length - 10, x, tip_y + 10, z)
    pen = pen_tip + barrel
    collision = (s ^ pen).volume()
    assert collision < .001, (name, collision)
    extraction = [(s ^ pen.translate((0, dy, 0))).volume() for dy in [1, 5, 10, 40, 180]]
    assert max(extraction) < .001
    # Separate radial clearance from nib-end clearance; a collision-free proxy
    # does not prove a load-bearing seat or physical magnetic retention.
    tip_gap = tip_y - floor
    result = dict(source=CATALOG[key]['path'], sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  floor_y_mm=round(floor, 4), bore_radii_at_0_5_2_4mm_above_floor_mm=[round(r, 4) for r in radii],
                  internal_seat='tapered' if tapered else 'flat cylinder floor',
                  assumed_pen_tip_length_mm=10, assumed_pen_barrel_diameter_mm=pen_d,
                  modeled_tip_y_mm=tip_y, axial_nib_clearance_mm=round(tip_gap, 4),
                  pen_collision_mm3=round(collision, 6), extraction_clear=True,
                  physical_retention_verified=False)
    if tip_gap < 1:
        result['finding'] = 'Taper exists, but the modeled nib has less than 1 mm end clearance; no protected load-bearing stop is demonstrated.'
    elif not tapered:
        result['finding'] = 'Pen proxy clears, but the bore terminates flat and the tip does not enter the outer cone.'
    else:
        result['finding'] = 'Tapered inner support and separate nib relief; nominal pen and extraction clear. Physical fit unverified.'
        assert tip_gap > 1.5
        result['minimum_new_seat_wall_mm'] = revisions[key]['minimum_new_seat_wall_mm']
    results[name] = result
    if bed_down:
        result['measurement_frame'] = 'normalized to original assembly coordinates using the inverse rigid print transform'
    # Actual cutaway, with the pen proxy overlaid on the opening.
    half = s ^ mf.Manifold.cube((200, 400, 200), True).translate((x - 100, 0, 0))
    center = np.array([floor + 3, z, x])
    objects = [(mesh(half).triangles[..., [1, 2, 0]] - center, (42, 100, 101)),
               (mesh(pen).triangles[..., [1, 2, 0]] - center, (211, 143, 73))]
    pic = render(objects, w=800, h=360, scale=18, rx=0, rz=0)
    draw = ImageDraw.Draw(pic)
    draw.text((18, 12), f'{name} / {result["internal_seat"]}', font=font, fill='#20494a')
    draw.rectangle((0, 315, 800, 360), fill=(244, 243, 239))
    draw.text((18, 326), f'Modeled nib clearance {tip_gap:.2f} mm | Orange = assumed stylus', font=font, fill='#20494a')
    pic.save(OUT / f'{key}_section.png')
    images.append(pic)

# These open-spine designs have a protective cup, rather than an outer cone.
for key, name in [('A_Open_Spine_Compact', 'ORBIT'), ('B_Rear_Spine_Extended', 'STRATOS')]:
    path = ROOT / CATALOG[key]['path']
    t = trimesh.load_mesh(path)
    floor = -67 - first_ray_distance(t.triangles, [0, -67, 9.8], [0, -1, 0])
    pen = cylinder(.15, 12, 0, -67, 9.8, 4.5) + cylinder(4.5, 145.5, 0, -55, 9.8)
    collision = (solid(t) ^ pen).volume()
    assert collision < .001
    results[name] = dict(source=CATALOG[key]['path'], internal_seat='protective cup; no outer cone',
                        floor_y_mm=round(floor, 4), modeled_tip_y_mm=-67,
                        axial_nib_clearance_mm=round(-67 - floor, 4),
                        pen_collision_mm3=round(collision, 6), physical_retention_verified=False,
                        finding='Tip is inside the cup with end clearance; retention is provided by clips/magnets and needs a physical test.')

(OUT / 'checks.json').write_text(json.dumps(results, indent=2) + '\n')
canvas = Image.new('RGB', (1600, 360 * 4), (244, 243, 239))
for i, pic in enumerate(images):
    canvas.paste(pic, ((i % 2) * 800, (i // 2) * 360))
canvas.save(OUT / 'all-sheath-sections.png')
for target in [ROOT / 'site/assets/reviews/tip-seats', ROOT / 'output/latest/tip-seat-review']:
    shutil.copytree(OUT, target, dirs_exist_ok=True)
    report = (ROOT / 'docs/TIP_SEAT_REVIEW.md').read_text().replace('../assets/', '../../../assets/')
    (target / 'REVIEW.md').write_text(report)
print(json.dumps(results, indent=2))
