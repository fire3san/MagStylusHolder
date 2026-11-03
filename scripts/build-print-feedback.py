"""Reversible print-feedback revisions; originals remain available. Units: mm.

Run with .venv/bin/python scripts/build-print-feedback.py.
Preserve the pointed outer style; shorten it and add a tapered internal seat.
"""
from pathlib import Path
import hashlib
import json
import math
import sys
import zipfile

import manifold3d as mf
import numpy as np
import trimesh
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/aura_duo'))
from render_common import render

OUT = ROOT / 'assets/downloads/Print_Feedback_v3'
OUT.mkdir(parents=True, exist_ok=True)


def box(size, center):
    return mf.Manifold.cube(size, True).translate(center)


def load(path):
    t = trimesh.load_mesh(ROOT / path)
    return mf.Manifold(mf.Mesh(np.asarray(t.vertices, np.float32),
                               np.asarray(t.faces, np.uint32)))


def mesh(s):
    q = s.to_mesh()
    return trimesh.Trimesh(np.asarray(q.vert_properties)[:, :3],
                           np.asarray(q.tri_verts), process=True)


def cross(style):
    if style == 'side':
        pts = [(-7, 0), (7, 0), (7, 3.4), (6.3, 8.6)]
        pts += [(6.3 * math.cos(t), 8.6 + 6.3 * math.sin(t))
                for t in np.linspace(0, math.pi, 65)[1:]]
        pts += [(-7, 3.4)]
    elif style == 'Flow':
        pts = [(-8, 0), (8, 0), (8, 3.2), (6.2, 9.8)]
        pts += [(6.2 * math.cos(t), 9.8 + 6.2 * math.sin(t))
                for t in np.linspace(0, math.pi, 65)[1:]]
        pts += [(-8, 3.2)]
    else:
        pts = [(-8.5, 0), (8.5, 0), (8.5, 3.2), (7, 10), (5.5, 14),
               (2.5, 16.1), (-2.5, 16.1), (-5.5, 14), (-7, 10), (-8.5, 3.2)]
    return mf.CrossSection([pts]).offset(-.35).offset(.35, circular_segments=32)


def revise_nose(source, x, z):
    shoulder, nose, seat_end, tip = -64.0, -72.04, -58.2, -68.2
    # Retain the upper sheath exactly. Rebuild below the new barrel seat so
    # the old flat bore floor can become a continuous tapered cavity.
    body = source ^ box((400, 400, 200), (0, seat_end + 200, 0))
    cs = cross('side')
    shell = cs.extrude(seat_end - shoulder + .1).rotate((90, 0, 0)).translate((x, seat_end + .1, 0))
    previous = None
    for old_y, sx, sz in [(-82, .08, .12), (-80, .24, .32),
                          (-76, .53, .63), (-70, .84, .9), (-64, 1, 1)]:
        # Retain the original outer section proportions and backing-plane tip.
        y = nose + .04 + (old_y + 82) / 18 * (shoulder - nose - .04)
        section = cs.scale((sx, sz)).extrude(.04).rotate((90, 0, 0)).translate((x, y, 0))
        if previous is not None:
            shell += (previous + section).hull()
        previous = section
    bore = (mf.Manifold.cylinder(200, 4.8, circular_segments=96)
            .rotate((-90, 0, 0)).translate((x, seat_end, z)))
    cone = (mf.Manifold.cylinder(10, .25, 4.8, circular_segments=96)
            .rotate((-90, 0, 0)).translate((x, tip, z)))
    # Check a 1.2 mm radial material margin around the internal tip seat.
    margin = (mf.Manifold.cylinder(10, 1.45, 6.0, circular_segments=96)
              .rotate((-90, 0, 0)).translate((x, tip, z)))
    assert (margin - shell).volume() < .001
    result = body + (shell - bore - cone)
    # Restore the one magnet pocket within the rebuilt region.
    result -= mf.Manifold.cylinder(3.01, 2.65, circular_segments=96).translate((x, -60, -.01))
    probe = box((400, 400, 200), (0, seat_end + 200 + .15, 0))
    delta = ((result ^ probe) - (source ^ probe)).volume()
    delta += ((source ^ probe) - (result ^ probe)).volume()
    assert delta < .001, delta
    assert (result ^ (bore + cone)).volume() < .001
    return result.simplify(.0001), delta


side = load('assets/stl/side/01_Side_Scabbard_PROVISIONAL.stl')
side_new, side_delta = revise_nose(side, -60.3, 8.6)

# Same flat 3.4 mm bridge and ring as the screen-facing v2 generator.
ring = side ^ box((200, 300, 100), (66, 0, 0))
cut = -60.3 + 8.3
holder = side_new ^ box((200, 300, 100), (cut - 100, 0, 0))
holder = holder.mirror((0, 0, 1)).translate((-64 - (-60.3), 0, 3.4))
bridge = box((28, 20, 3.4), (-44, 0, 1.7))  # x=-58 .. -30
screen_new = (ring + bridge + holder).simplify(.0001)
screen_old = load('assets/stl/screen-facing/AURA_SCREEN.stl')
case = box((112, 152, 9.8), (0, 0, -4.9))
assert (screen_new ^ case).volume() < .001
ring_probe = box((100, 100, 100), (30, 0, 0))
assert ((screen_new ^ ring_probe) - (screen_old ^ ring_probe)).volume() < .001
assert ((screen_old ^ ring_probe) - (screen_new ^ ring_probe)).volume() < .001
flat_probe = box((19, 19, 100), (-44.5, 0, 0))
assert np.allclose(mesh(screen_new ^ flat_probe).bounds[:, 2], [0, 3.4])

items = [
    ('AURA_SCREEN_v3', screen_old, screen_new, side_delta),
]
checks = {}
for name, old, new, delta in items:
    assert new.status() == mf.Error.NoError and len(new.decompose()) == 1, name
    path = OUT / f'{name}.stl'
    mesh(new).export(path)
    exported = trimesh.load_mesh(path)
    # STL stores float32 positions. Weld coincident seam vertices to 0.0001 mm
    # before writing; discard triangles collapsed by that sub-micron weld.
    exported.merge_vertices(digits_vertex=4)
    exported.update_faces(exported.nondegenerate_faces())
    exported.remove_unreferenced_vertices()
    exported.export(path)
    t = trimesh.load_mesh(path)
    assert t.is_watertight and t.is_winding_consistent and t.volume > 0, name
    reloaded = load(path.relative_to(ROOT))
    assert reloaded.status() == mf.Error.NoError and len(reloaded.decompose()) == 1
    # Verify a 9 mm barrel with an assumed 10 mm tapered pen tip.
    barrel = (mf.Manifold.cylinder(160, 4.5, circular_segments=96)
              .rotate((-90, 0, 0)).translate((-64, -58.19, -5.2)))
    pen_tip = (mf.Manifold.cylinder(10, .1, 4.5, circular_segments=96)
               .rotate((-90, 0, 0)).translate((-64, -68.19, -5.2)))
    for shift in [0, 2, 10, 40, 160]:
        assert (reloaded ^ (barrel + pen_tip).translate((0, shift, 0))).volume() < .001
    for y in [-60, -48, -36, -24, -12]:
        magnet = mf.Manifold.cylinder(1, 2.5, circular_segments=96).translate((-64, y, .6))
        assert (reloaded ^ magnet).volume() < .001
    checks[name] = dict(watertight=True, consistent_winding=True, connected_solids=1,
                        extents_mm=t.extents.round(3).tolist(),
                        bounds_mm=t.bounds.round(3).tolist(),
                        volume_cm3=round(t.volume / 1000, 3),
                        unchanged_body_difference_mm3=round(delta, 6),
                        sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    # Compare exact exported meshes from the same camera and assembly center.
    center = mesh(old).bounds.mean(axis=0)
    canvas = Image.new('RGB', (1200, 610), (244, 243, 239))
    for i, solid in enumerate([old, new]):
        v = mesh(solid).triangles - center
        canvas.paste(render([(v, (42, 100, 101))], w=600, h=550,
                            scale=4.4, rx=145 if name == 'AURA_SCREEN_v3' else -48,
                            rz=-20), (600 * i, 50))
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 16), name + ' / BEFORE', fill='#20494a')
    draw.text((624, 16), name + ' / REVISED', fill='#20494a')
    canvas.save(OUT / f'{name}_comparison.png')
    section_view = Image.new('RGB', (1200, 410), (244, 243, 239))
    draw = ImageDraw.Draw(section_view)
    for i, (solid, axis) in enumerate([(old, -66), (reloaded, -64)]):
        cutaway = solid ^ box((200, 400, 200), (axis - 100, 0, 0))
        v = mesh(cutaway).triangles[..., [1, 2, 0]]
        v -= np.array([-65, -4, axis])
        section_view.paste(render([(v, (42, 100, 101))], w=600, h=350,
                                  scale=17, rx=0, rz=0), (600 * i, 45))
    draw.text((20, 15), 'ORIGINAL / FLAT INTERNAL FLOOR', fill='#20494a')
    draw.text((620, 15), 'REVISED / 10 mm TAPERED INTERNAL SEAT', fill='#20494a')
    section_view.save(OUT / f'{name}_internal_section.png')

checks['AURA_SCREEN_v3'].update(pen_axis_x_mm=-64, previous_pen_axis_x_mm=-66,
    holder_to_assumed_case_gap_mm=1, previous_gap_mm=3,
    nose_y_mm=-72.04, previous_nose_y_mm=-82.04, tip_shortening_mm=10,
    internal_tip_seat_length_mm=10, internal_tip_end_y_mm=-68.2,
    barrel_seat_start_y_mm=-58.2, assumed_pen_tip_length_mm=10,
    assumed_case_bottom_y_mm=-76, bottom_clearance_mm=3.96,
    bridge_z_bounds_mm=[0, 3.4], case_intersection_mm3=0,
    ring_difference_mm3=0)
(OUT / 'checks.json').write_text(json.dumps(checks, indent=2) + '\n')
(OUT / 'README.md').write_text('''# Print feedback revision / 2026-11-03

Start with **AURA_SCREEN_v3.stl**. All coordinates and dimensions are in mm.

- AURA SCREEN: move the holder 2 mm toward the device; nominal case gap 3 → 1 mm.
- Shorten the sheath by exactly 10 mm overall: nose Y=-82.04 → -72.04.
  This gives 3.96 mm clearance above the existing 152 mm case envelope bottom.
  Actual bottom clearance depends on where the ring is mounted on your case.
- Keep the original pointed outer style; compress only the outer nose length.
- Replace the flat internal bore floor with a 10 mm tapered seat, from a
  9.6 mm barrel bore at Y=-58.2 to a 0.5 mm end at Y=-68.2. The pen tip can
  enter the cone instead of stopping at a flat cylinder floor.
- The internal taper assumes a 10 mm stylus nose. This is a CAD fit assumption,
  not a measurement of the photographed pen. A 9 mm barrel + 10 mm tip proxy
  clears the seat and extraction path. Actual seating depends on your pen tip.
- Preserve the upper entry slot, five magnet pockets and ring. The screen
  bridge stays flat at Z=0 / 3.4 mm. At least 1.2 mm radial material surrounds
  the modeled tapered seat before the magnet pockets are cut.

Brown-circle review: the side AURA and DUO use the same backing-plane taper
construction. AERIS and VERTEX already use a continuous loft with a shorter
8 mm nose, but their end also converges toward the backing plane. These are
connected solids, not separate loose parts. This pack revises the physically
tested AURA SCREEN only; the other family files remain unchanged.

Original STL files and existing download packs are unchanged. Comparison PNGs
show actual meshes, with the old model left and revised model right. checks.json
records closed meshes, consistent winding, one solid, dimensions and file hashes.
CAD envelope checks do not measure the printed case fit or retention.

Reported first print: PLA, 8.62 m (user's slicer result). This revision has not
been sliced: filament length depends on orientation, supports and slicer settings.
Please re-slice the revised STL to obtain the new material estimate.

Rebuild: .venv/bin/python scripts/build-print-feedback.py
''')
archive = OUT.with_suffix('.zip')
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for path in sorted(OUT.iterdir()):
        z.write(path, path.name)
print(json.dumps(checks, indent=2))
