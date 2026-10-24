"""Build screen-facing side variants. Run with .venv/bin/python.

Z=0 is the case back; +Z points away from the back. The provisional
screen plane is Z=-10 mm. Keep the magnetic ring intact, mirror only the
outboard holder about Z=1.7 mm, and join it with a flat 3.4 mm bridge.
No vertical return, step or L-shaped connector is used.
"""
from pathlib import Path
import json
import shutil
import sys
import zipfile
from PIL import Image, ImageDraw, ImageFont

import manifold3d as mf
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/aura_duo'))
from render_common import render

BASE_T = 3.4
CASE_EDGE = 1.5  # Provisional case allowance per edge, not measured.
OUT = ROOT / 'assets/stl/screen-facing'
IMAGES = ROOT / 'assets/renders/screen-facing'
OUT.mkdir(parents=True, exist_ok=True)
IMAGES.mkdir(parents=True, exist_ok=True)
MODELS = [
    ('AURA_SCREEN', '01_Side_Scabbard_PROVISIONAL.stl', -60.3, 56.0, 152.0, 9.8, 'BOOX Go 6 (Gen II)'),
    ('NEXUS_SCREEN', '02_Side_QuickClip_PROVISIONAL.stl', -60.3, 56.0, 152.0, 9.8, 'BOOX Go 6 (Gen II)'),
    ('AURA_DUO_SCREEN', 'AURA_DUO_iPhone_v3.stl', -53.55, 43.55, 120.8, 14.3, 'iPhone Duo (closed)'),
]


def box(size, center):
    return mf.Manifold.cube(size, True).translate(center)


def mesh(solid):
    m = solid.to_mesh()
    return trimesh.Trimesh(np.asarray(m.vert_properties)[:, :3],
                           np.asarray(m.tri_verts), process=True)


checks = {}
for name, filename, old_x, half_width, height, thickness, device_name in MODELS:
    original = trimesh.load_mesh(ROOT / 'assets/stl/side' / filename)
    source = mf.Manifold(mf.Mesh(np.asarray(original.vertices, dtype=np.float32),
                                 np.asarray(original.faces, dtype=np.uint32)))
    # Preserve everything in the magnetic ring, including its recess/notch.
    ring_region = box((200, 300, 100), (66, 0, 0))  # x >= -34
    ring = source ^ ring_region
    cut = old_x + 8.3
    holder = source ^ box((200, 300, 100), (cut - 100, 0, 0))
    # Keep 3 mm between the holder's inner wall and the nominal case edge.
    # Reflect about the bridge mid-plane instead of lowering the whole holder.
    new_x = -(half_width + 10.0)
    holder = holder.mirror((0, 0, 1)).translate((new_x - old_x, 0, BASE_T))
    bridge_end = new_x + 6.0
    bridge = box((-30 - bridge_end, 20, BASE_T),
                 ((-30 + bridge_end) / 2, 0, BASE_T / 2))
    result = ring + bridge + holder
    # Inspect the bridge span away from both ring and holder: both faces stay
    # at Z=0 / 3.4 mm, with no L-shaped riser hidden in the exported STL.
    bridge_start = new_x + 9.0
    flat_region = box((-34 - bridge_start, 19, 100),
                      ((-34 + bridge_start) / 2, 0, 0))
    flat_bounds = mesh(result ^ flat_region).bounds[:, 2]
    assert np.allclose(flat_bounds, [0, BASE_T], atol=1e-5), flat_bounds
    assert result.status() == mf.Error.NoError
    assert len(result.decompose()) == 1, name
    part = mesh(result)
    assert part.is_watertight and part.is_winding_consistent and part.volume > 0
    # The new bridge never enters the original ring region.
    preserved = box((100, 100, 50), (30, 0, 0))  # x >= -20
    difference = ((result ^ preserved) - (source ^ preserved)).volume()
    difference += ((source ^ preserved) - (result ^ preserved)).volume()
    assert difference < 1e-4
    # Test against the assumed cased device envelope, not just its side plane.
    device = box((half_width * 2, height, thickness), (0, 0, -thickness / 2))
    intersection = (result ^ device).volume()
    assert intersection < 1e-4, (name, intersection)
    part.export(OUT / f'{name}.stl')
    render([(part.triangles, (213, 143, 73))], w=900, h=240,
           scale=6, rx=90, rz=0).save(IMAGES / f'{name}_profile.png')
    device_mesh = mesh(device)
    screen_mesh = mesh(box((half_width * 2 - 6, height - 6, .3), (0, 0, -thickness - .2)))
    # View from screen side so the reversed holder is visible.
    render([(device_mesh.triangles, (145, 152, 151)),
            (screen_mesh.triangles, (203, 215, 203)),
            (part.triangles, (213, 143, 73))],
           w=900, h=740, scale=3.5, rx=145, rz=-20).save(IMAGES / f'{name}.png')
    checks[name] = {
        'source': filename, 'watertight': bool(part.is_watertight),
        'consistent_winding': bool(part.is_winding_consistent),
        'connected_solids': len(result.decompose()),
        'extents_mm': part.extents.round(3).tolist(),
        'pen_axis_x_mm': new_x,
        'assumed_case_width_mm': half_width * 2,
        'assumed_case_height_mm': height, 'assumed_case_thickness_mm': thickness,
        'holder_to_case_gap_mm': round(-half_width - (new_x + 7), 3),
        'bridge_z_bounds_mm': flat_bounds.round(3).tolist(),
        'bridge_vertical_step_mm': 0.0,
        'device': device_name,
        'revision': 'v2-flat / no L connector',
        'case_intersection_mm3': round(intersection, 6),
        'ring_difference_mm3': round(difference, 6),
        'status': 'CAD concept; physical fit, strength, retention and hinge sweep unverified',
    }

comparison = Image.new('RGB', (900, 810), (244, 243, 239))
draw = ImageDraw.Draw(comparison)
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 23)
for i, (name, *_) in enumerate(MODELS):
    comparison.paste(Image.open(IMAGES / f'{name}_profile.png'), (0, i * 270 + 30))
    draw.text((24, i * 270 + 12), name + ' / v2 FLAT / 0 mm step', fill=(42, 57, 49), font=font)
comparison.save(IMAGES / 'flat_profiles_v2.png')
(OUT / 'checks.json').write_text(json.dumps(checks, indent=2) + '\n')
guide = """# 朝屏幕水平接駁 v2 / Flat screen-facing v2

NEXUS SCREEN、AURA SCREEN：BOOX Go 6 (Gen II)。
AURA DUO SCREEN：iPhone Duo（收合尺寸包絡；展開與摺疊待驗證）。
三款已修改實際 STL：連接臂上下表面為 Z=0 / 3.4 mm，沒有 L 形或高低落差。
磁環維持機背位置，筆鞘／筆夾以 Z=1.7 mm 反射，向屏幕方向凸出。
筆身仍沿機身長邊；「水平」指連接臂同層，不是把筆轉成橫放。

設備尺寸依據：
- BOOX 官方 Go 6 (Gen II)：149 × 109 × 6.8 mm。
  https://shop.boox.com/products/go6gen2
- Apple 官方 iPhone Duo：收合 117.8 × 84.1 × 11.3 mm；
  展開 117.8 × 164.6 × 5.2 mm。
  https://www.apple.com/iphone-duo/specs/

以上為機身尺寸。每面暫加1.5 mm保護殼包絡，並非已量度的保護殼。
BOOX 檢查包絡為112 × 152 × 9.8 mm；DUO 為87.1 × 120.8 × 14.3 mm。
筆軸偏置：BOOX 66 mm；DUO 53.55 mm，筆鞘內側距假設殼邊3 mm。
磁環在示意殼中央；實際磁環位置須按實機核對。
磁環介面、原筆鞘／夾口尺寸及磁孔保留；筆鞘反射後的磁石極性須重核。

checks.json 記錄封閉網格、單一實體、磁環未改動、水平連接臂高度及包絡交疊檢查。
灰綠色機身為包絡示意，橙色是實際 STL。*_profile.png 是實際 STL 的側視圖。
實體配合、側鍵與接口、磁石裝配、保持力、臂強度及 DUO 鉸鏈掃掠仍待驗證。
請交由列印商審核 PA12 製程、公差與支撐，不能以包絡檢查取代實機打樣。

Rebuild: .venv/bin/python scripts/build-screen-facing.py
The three v2 STL files use a coplanar bridge with zero vertical step.
Holder projection is toward the screen; the pen remains parallel to the long edge.
Device sizes are from the official sources above. Case allowances are provisional.
"""
(OUT / 'README.md').write_text(guide)
archive = ROOT / 'assets/downloads/Screen_Facing_Flat_v2.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for path in sorted(OUT.iterdir()):
        z.write(path, path.name)
    for path in sorted(IMAGES.iterdir()):
        z.write(path, 'renders/' + path.name)
# Also refresh the already extracted local pack used for inspecting the STL.
extracted = ROOT / 'assets/downloads/Screen_Facing_Concepts'
if extracted.is_dir():
    shutil.copytree(OUT, extracted, dirs_exist_ok=True)
    shutil.copytree(IMAGES, extracted / 'renders', dirs_exist_ok=True)
for folder in (OUT, IMAGES):
    target = ROOT / 'site' / folder.relative_to(ROOT)
    shutil.copytree(folder, target, dirs_exist_ok=True)
shutil.copy2(archive, ROOT / 'site' / archive.relative_to(ROOT))
# Keep the earlier download URL current as well.
for folder in (ROOT / 'assets/downloads', ROOT / 'site/assets/downloads'):
    shutil.copy2(archive, folder / 'Screen_Facing_Concepts.zip')
print(json.dumps(checks, indent=2))
