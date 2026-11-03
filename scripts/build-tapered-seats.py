"""Closed-sheath revisions with >=1.5 mm material around each new tip seat.

Preserve the outer shape, ring, pockets and upper bore. Refill only the former
internal bore below the new shoulder, then cut a tapered seat and nib relief.
Run with .venv/bin/python scripts/build-tapered-seats.py.
"""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import zipfile

import manifold3d as mf
import numpy as np
import trimesh
from PIL import ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/aura_duo'))
from render_common import render

OUT = ROOT / 'assets/downloads/Tapered_Seats_20261103'
OUT.mkdir(parents=True, exist_ok=True)
CONFIG = [
    ('AURA_SCREEN', 'AURA_SCREEN_v4', 'assets/downloads/Print_Feedback_v3/AURA_SCREEN_v3.stl', -64, 8.6, -68.2, 9.6, 9, True),
    ('Side_Scabbard_v3', 'AURA_v4', 'assets/stl/side/01_Side_Scabbard_PROVISIONAL.stl', -60.3, 8.6, -66, 9.6, 9, False),
    ('AURA_DUO_iPhone', 'AURA_DUO_v4', 'assets/stl/side/AURA_DUO_iPhone_v3.stl', -53.55, 8.6, -66, 9.6, 8.9, False),
    ('AURA_DUO_SCREEN', 'AURA_DUO_SCREEN_v3', 'assets/stl/screen-facing/AURA_DUO_SCREEN.stl', -53.55, 8.6, -66, 9.6, 8.9, True),
    ('S_Flow_BOOX_vertical', 'AERIS_v10', 'assets/stl/v9/S_Flow_BOOX_vertical.stl', 0, 9.8, -61.96, 9.6, 9, False),
    ('S_Facet_BOOX_vertical', 'VERTEX_v10', 'assets/stl/v9/S_Facet_BOOX_vertical.stl', 0, 9.8, -51.96, 9.6, 9, False),
    ('S_Flow_iPad_Pencil89', 'TITAN_PRO_v10', 'assets/stl/v9/S_Flow_iPad_Pencil89.stl', 0, 9.8, -82.5, 9.3, 8.9, False),
]


def box(size, center):
    return mf.Manifold.cube(size, True).translate(center)


def cylinder(r, length, y=0, top=None):
    return (mf.Manifold.cylinder(length, r, r if top is None else top, circular_segments=96)
            .rotate((-90, 0, 0)).translate((0, y, 0)))


def solid(t):
    return mf.Manifold(mf.Mesh(np.asarray(t.vertices, np.float32), np.asarray(t.faces, np.uint32)))


def mesh(s):
    q = s.to_mesh()
    return trimesh.Trimesh(np.asarray(q.vert_properties)[:, :3], np.asarray(q.tri_verts), process=True)


def flip(s):
    return s.mirror((0, 0, 1)).translate((0, 0, 3.4))


def export_checked(s, path):
    mesh(s).export(path)
    raw = trimesh.load_mesh(path)
    raw_solid = solid(raw)
    if raw.is_watertight and raw.is_winding_consistent and raw_solid.status() == mf.Error.NoError and len(raw_solid.decompose()) == 1:
        return raw, raw_solid
    # Float32 STL seams sometimes need a sub-micron weld. Choose the finest
    # successful weld and validate the file after its final export/reload.
    for digits in [7, 6, 5, 4]:
        t = raw.copy()
        t.merge_vertices(digits_vertex=digits)
        t.update_faces(t.nondegenerate_faces())
        t.remove_unreferenced_vertices()
        if not t.is_watertight:
            continue
        t.export(path)
        t = trimesh.load_mesh(path)
        s = solid(t)
        if t.is_watertight and t.is_winding_consistent and s.status() == mf.Error.NoError and len(s.decompose()) == 1:
            return t, s
    raise AssertionError(f'Invalid exported mesh: {path}')


checks = {}
sphere = mf.Manifold.sphere(1.55, circular_segments=32)
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 18)
for key, name, source, x, z, old_floor, bore_d, pen_d, screen in CONFIG:
    source_mesh = trimesh.load_mesh(ROOT / source)
    original = solid(source_mesh)
    normalized = flip(original) if screen else original
    # The cone has 0.15 mm radial assembly clearance to the assumed pen nose.
    # At contact, its sides stop downward movement before the nib hits the end.
    slope = (pen_d / 2 - .1) / 10
    top_radius = pen_d / 2 + .15
    cone_template = cylinder(.25, 10, top=top_radius)
    relief_template = cylinder(.8, 3.5, -2)  # 2 mm below the cone's nominal end
    seat_template = cone_template + relief_template
    # A spherical dilation tests all directions, including axial end thickness
    # and webs above/alongside the existing magnet pockets. 0.05 mm is reserved
    # for tessellation/export tolerance above the required 1.50 mm.
    envelope_template = (cone_template.minkowski_sum(sphere)
                         + relief_template.minkowski_sum(sphere))
    accepted = None
    best = (float('inf'), None)
    for i in range(61):
        tip = round(old_floor - 9 + .25 * i, 4)
        upper = tip + 10
        if upper < old_floor:
            continue
        if key == 'AURA_SCREEN':
            previous_void = (cylinder(.27, 10, old_floor, 4.82)
                             + cylinder(4.82, 100, old_floor + 10))
        else:
            previous_void = cylinder(bore_d / 2 + .02, 100, old_floor)
        filler = previous_void ^ box((300, 400, 200), (0, upper - 200 + .1, 0))
        blank = normalized + filler.translate((x, 0, z))
        seat = seat_template.translate((x, tip, z))
        bore = cylinder(bore_d / 2, 200, upper).translate((x, 0, z))
        void = seat + bore
        # Keep the old upper bore facets. Only the new internal infill needs
        # a bore cut; avoid recutting the long existing float32 cylinder.
        result = (normalized - seat) + (filler.translate((x, 0, z)) - void)
        wall = envelope_template.translate((x, tip, z)) - void
        missing = (wall - result).volume()
        best = min(best, (missing, tip))
        if missing < 1e-5:
            accepted = (tip, result, wall, void, upper)
            break
    assert accepted is not None, (name, best)
    tip, result, wall, void, upper = accepted
    assert result.status() == mf.Error.NoError and len(result.decompose()) == 1
    # No exterior is added: the filler stays inside the original bore.
    assert (result - normalized).volume() < filler.volume() + .001
    # Test upper body/ring/pockets as actual volumes, beyond the new seat.
    upper_probe = box((400, 400, 200), (0, upper + 200 + .2, 0))
    difference = ((result ^ upper_probe) - (normalized ^ upper_probe)).volume()
    difference += ((normalized ^ upper_probe) - (result ^ upper_probe)).volume()
    assert difference < .001
    final = flip(result) if screen else result
    path = OUT / f'{name}.stl'
    exported_mesh, exported = export_checked(final.as_original().set_tolerance(.0001).simplify(.0001), path)
    checked = flip(exported) if screen else exported
    assert (wall - checked).volume() < .003, (name, 'exported wall')
    # Use a position 0.02 mm above ideal side contact; avoid a zero-clearance
    # Boolean degeneracy while retaining a positive, measured nib gap.
    contact_shift = .15 / slope
    pen_tip_y = tip - contact_shift + .02
    pen_tip = cylinder(.1, 10, pen_tip_y, pen_d / 2).translate((x, 0, z))
    barrel = cylinder(pen_d / 2, 160, pen_tip_y + 10).translate((x, 0, z))
    pen = pen_tip + barrel
    collision = (checked ^ pen).volume()
    assert collision < .001, (name, collision)
    for shift in [1, 5, 10, 40, 180]:
        assert (checked ^ pen.translate((0, shift, 0))).volume() < .001
    # Deliberate small downward overtravel must hit the supporting nose sides,
    # while the nib remains well above the relieved floor.
    overtravel_collision = (checked ^ pen.translate((0, -.1, 0))).volume()
    assert overtravel_collision > .001, (name, 'no supporting stop')
    nib_gap = pen_tip_y - (tip - 2)
    assert nib_gap > 1.5
    ring_probe = box((150, 100, 150), (40, 5, 0)) if x else box((150, 48, 150), (0, 0, 0))
    ring_difference = ((final ^ ring_probe) - (original ^ ring_probe)).volume()
    ring_difference += ((original ^ ring_probe) - (final ^ ring_probe)).volume()
    assert ring_difference < .001
    assert np.allclose(exported_mesh.bounds, source_mesh.bounds, atol=.001)
    checks[key] = dict(file=path.name, source=source, revision=name,
        sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        watertight=True, connected_solids=1, consistent_winding=True,
        extents_mm=exported_mesh.extents.round(3).tolist(),
        minimum_new_seat_wall_mm=1.5, verification_envelope_radius_mm=1.55,
        wall_envelope_missing_mm3=round((wall - checked).volume(), 7),
        nominal_cone_end_y_mm=tip, internal_floor_y_mm=round(tip - 2, 4),
        barrel_bore_start_y_mm=upper, pen_axis_x_mm=x,
        pen_axis_z_mm=round(3.4 - z if screen else z, 4),
        assumed_pen_tip_length_mm=10, assumed_pen_diameter_mm=pen_d,
        modeled_pen_tip_y_mm=round(pen_tip_y, 5),
        nib_end_clearance_mm=round(nib_gap, 4),
        pen_collision_mm3=round(collision, 7), extraction_clear=True,
        downward_overtravel_0_1mm_collision_mm3=round(overtravel_collision, 5),
        ring_difference_mm3=round(ring_difference, 7),
        upper_body_difference_mm3=round(difference, 7),
        original_outer_bounds_preserved=True, physical_fit_verified=False)
    half = checked ^ box((200, 400, 200), (x - 100, 0, 0))
    center = np.array([tip + 4, z, x])
    v = mesh(half).triangles[..., [1, 2, 0]] - center
    p = mesh(pen).triangles[..., [1, 2, 0]] - center
    pic = render([(v, (42, 100, 101)), (p, (213, 143, 73))], w=900, h=410, scale=20, rx=0, rz=0)
    draw = ImageDraw.Draw(pic)
    draw.text((16, 12), f'{name} / tapered support + nib relief', font=font, fill='#20494a')
    draw.rectangle((0, 356, 900, 410), fill=(244, 243, 239))
    draw.text((16, 370), f'New seat wall >= 1.5 mm | Modeled nib gap {nib_gap:.2f} mm', font=font, fill='#20494a')
    pic.save(OUT / f'{name}_section.png')
    v = exported_mesh.triangles - exported_mesh.bounds.mean(axis=0)
    render([(v, (42, 100, 101))], w=900, h=740, scale=5.2, rx=145 if screen else -48,
           rz=-20).save(OUT / f'{name}.png')
    print(f'{name}: seat end {tip}, nib gap {nib_gap:.3f}, wall envelope passed', flush=True)

(OUT / 'checks.json').write_text(json.dumps(checks, indent=2) + '\n')
(OUT / 'README.md').write_text('''# Tapered inner seats / 2026-11-03

Seven closed sheaths have tapered internal support plus a separate relief
pocket beneath the nib. The nominal 10 mm pen nose is supported along its
wider tapered sides before the nib reaches the floor. A 0.1 mm downward
overtravel check demonstrates side contact while the modeled nib still has
more than 1.5 mm of axial relief.

At least 1.5 mm of material surrounds each newly cut seat, including its end
and the webs beside existing magnet pockets. This is checked with a 1.55 mm
spherical offset envelope, allowing 0.05 mm for tessellation/export tolerance.
It is a local tip-seat thickness check, not a minimum for every legacy feature
on the whole holder. Existing upper barrel walls, slots, ring and pockets stay.

Original exterior bounds are preserved. AURA SCREEN retains the prior 10 mm
overall shortening and 2 mm inward move. Other models retain their lengths.
Open clips and protective cups are not modified by this revision.

Pen profiles remain assumptions: 10 mm nose, 9 mm BOOX barrel / 8.9 mm Pencil
barrel. Actual pen geometry, FDM tolerance, insertion force and retention need
physical testing. Units: mm; do not auto-scale. No magnets or spacers included.

checks.json records per-model positions, hashes, wall and collision checks.
Section PNGs show the actual exported STL with the assumed pen in orange.
Old versioned downloads remain available; use this pack for current sheaths.

Rebuild: .venv/bin/python scripts/build-tapered-seats.py
''')
with zipfile.ZipFile(OUT.with_suffix('.zip'), 'w', zipfile.ZIP_DEFLATED) as zf:
    for p in sorted(OUT.iterdir()):
        zf.write(p, p.name)
shutil.copytree(OUT, ROOT / 'site' / OUT.relative_to(ROOT), dirs_exist_ok=True)
shutil.copy2(OUT.with_suffix('.zip'), ROOT / 'site' / OUT.with_suffix('.zip').relative_to(ROOT))
shutil.copytree(OUT, ROOT / 'output/latest/tapered-seats', dirs_exist_ok=True)
shutil.copy2(OUT.with_suffix('.zip'), ROOT / 'output/latest' / OUT.with_suffix('.zip').name)
