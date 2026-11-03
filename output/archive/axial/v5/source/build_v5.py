"""v5 build — two design updates from v4, same functional dimensions.

KM_tunnel: the central collar tunnel now extends continuously through
           both end clips at Y=-23 and Y=+23, forming one long bore.
Shield_scabbard: shield-shaped base outline with decorative raised border,
                 central ridge, chamfered edges — same bore/magnets.
"""
from geometry import *
import geometry as g
OUT = Path(__file__).resolve().parents[1]

# ── helpers (carried from v4) ───────────────────────────────────────
def softbox(w, l, h, r, at):
    s = None
    for x in [-w/2+r, w/2-r]:
        for y in [-l/2+r, l/2-r]:
            for z in [r, h-r]:
                p = m.Manifold.sphere(r, 24).translate((x, y, z))
                s = p if s is None else s + p
    return s.hull().translate(at)

def sockets(s, ys):
    for y in ys:
        s -= cyl(3.15, 4.01, (0, y, -.01))
    return s

def softcapsule(w, l, h, r, at):
    parts = []
    for y in [-l/2+w/2, l/2-w/2]:
        for z in [r, h-r]:
            for a in np.linspace(0, 2*math.pi, 24, endpoint=False):
                parts.append(m.Manifold.sphere(r, 16).translate((
                    (w/2-r)*math.cos(a), y+(w/2-r)*math.sin(a), z)))
    s = parts[0]
    for p in parts[1:]:
        s += p
    return s.hull().translate(at)

def tris(s):
    q = s.to_mesh()
    return np.asarray(q.vert_properties)[:, :3][np.asarray(q.tri_verts)].round(5).tolist()

results = {}
scenes = {}

def save(name, s):
    assert s.status() == m.Error.NoError and len(s.decompose()) == 1
    q = s.to_mesh()
    t = trimesh.Trimesh(np.asarray(q.vert_properties)[:, :3],
                        np.asarray(q.tri_verts), process=True)
    t.export(OUT / 'stl' / f'{name}.stl')
    t = trimesh.load_mesh(OUT / 'stl' / f'{name}.stl')
    assert t.is_watertight and t.is_winding_consistent and t.volume > 0
    results[name] = {
        'size_mm': t.extents.round(3).tolist(),
        'volume_cm3': round(t.volume / 1000, 3),
        'watertight': True, 'winding_consistent': True, 'connected_solids': 1
    }

# ── KM tunnel: continuous bore through collar and both clips ────────
def km_tunnel():
    s = (cyl(34, 3.2) - cyl(17, 5, (0, 0, -1))) + rounded(20, 65, 3.2, 3)

    # Continuous tunnel spine: one tube from clip-to-clip (Y=-26.5 to +26.5)
    tunnel_len = 55  # covers both clips with margin
    s += along_y(5.7, tunnel_len, y=-1)  # sleeve, widened to bridge all clips
    s += along_y(7, 3)                    # centre flange
    s += rounded(14, 58, 4.6, 3)          # solid support rail under tunnel

    # Bore through entire tunnel length
    s -= along_y(4.7, tunnel_len + 4, y=-1)
    # Top split runs the whole tunnel length
    s -= box(1.6, tunnel_len + 4, 15, (0, -1, 16.8))

    # Clips at all three positions — pen passes through all of them
    for y_pos in [-23, 0, 23]:
        s += g.clip().translate((0, y_pos, 0))

    return sockets(s - g.ring_cut(), [-12, 0, 12])

# ── Shield scabbard: heraldic outline with decorative detail ────────
def shield_outline(w, l, tip_l, h, r=1.5):
    """Shield/pointed-bottom shape: rectangle top + pointed tip bottom."""
    hw = w / 2
    # Points: top-left, top-right, mid-right, tip, mid-left
    pts = [
        (-hw + r, l/2 - r),          # top-left
        (hw - r, l/2 - r),           # top-right
        (hw - r, -l/2 + tip_l + r),  # right waist
        (0, -l/2 - tip_l/2),         # tip (pointed bottom)
        (-hw + r, -l/2 + tip_l + r), # left waist
    ]
    circles = None
    for x, y in pts:
        c = m.CrossSection.circle(r, 32).translate((x, y))
        circles = c if circles is None else circles + c
    return circles.hull().extrude(h)

def shield_scabbard():
    # Base puck (same MagSafe ring)
    s = (cyl(34, 3.2) - cyl(17, 5, (0, 0, -1)))

    # Shield-shaped base plate instead of capsule
    shield_w = 18    # width of the shield rail
    shield_l = 120   # rectangular portion length
    shield_tip = 16  # how far the pointed tip extends
    shield = shield_outline(shield_w, shield_l, shield_tip, BASE, r=2.0)
    shield = shield.translate((0, -25, 0))
    s += shield

    # Raised border/frame: slightly wider outline minus interior, below bore height
    border_outer = shield_outline(shield_w + 3, shield_l + 3, shield_tip + 2, 1.0, r=2.5).translate((0, -25, BASE))
    border_inner = shield_outline(shield_w - 1, shield_l - 1, shield_tip - 1, 2, r=1.5).translate((0, -25, BASE - 0.5))
    border = border_outer - border_inner
    # Cut border clear of tube footprint
    border -= along_y(7.5, 130, -20, 9.8)
    s += border

    # Central ridge line along the shield body (below bore)
    ridge = softbox(2.0, shield_l - 10, 0.8, 0.4, (0, -25, BASE))
    # Cut ridge clear of tube
    ridge -= along_y(7.5, 130, -20, 9.8)
    s += ridge
    s += ridge

    # Tube (same bore as v4 scabbard)
    tube = along_y(6.2, 116, -20, 9.8) + m.Manifold.sphere(6.2, 96).translate((0, -78, 9.8))
    # Solid foot under tube
    foot = softbox(14, 118, 4.4, 1.2, (0, -20, 0))
    s += tube + foot

    # Bore
    s -= along_y(4.8, 119, -20.5, 9.8)
    # Conical entry lead-in
    lead = m.Manifold.cylinder(.8, 5.3, 4.8, circular_segments=96).rotate((90, 0, 0)).translate((0, 38.01, 9.8))
    s -= lead

    # Decorative shoulder fillets at the tube-base junction (below bore)
    for y_off in [36, -76]:
        fillet = m.Manifold.sphere(2.0, 32).translate((0, y_off, 2.5))
        s += fillet

    return sockets(s - g.ring_cut(), [-68, -54, -40])

# ── Build all ───────────────────────────────────────────────────────
print("Building v5 models...")

for name, s, z in [
    ('KM_tunnel_through_clips', km_tunnel(), 9.3),
    ('Shield_scabbard', shield_scabbard(), 9.8),
]:
    save(name, s)
    pen = along_y(4.5, 157.5, 0, z)
    pen_collision = (s ^ pen).volume()
    assert pen_collision < 1e-6, f"{name}: pen collision {pen_collision}"
    for dy in [10, 30, 60, 100, 160]:
        assert (s ^ pen.translate((0, dy, 0))).volume() < 1e-6
    ys = [-12, 0, 12] if name.startswith('KM') else [-68, -54, -40]
    for y in ys:
        assert (s ^ cyl(3, 2, (0, y, 2))).volume() < 1e-6
    results[name]['nominal_pen_collision_mm3'] = 0
    scenes[name] = tris(s)

save('magnet_spacer_6.05x1.9_print_3_per_holder', cyl(3.025, 1.9))

# Test pieces
for bore, z, label in [(9.4, 9.3, 'KM'), (9.6, 9.8, 'S')]:
    s = rounded(16, 14, 4.6, 2) + along_y(6.2, 12, 0, z) - along_y(bore/2, 16, 0, z)
    s = sockets(s, [0])
    save(f'{label}_bore_and_socket_sample', s)

(OUT / 'checks.json').write_text(json.dumps(results, indent=2))
(OUT / 'scenes.json').write_text(json.dumps(scenes))
print(json.dumps(results, indent=2))
