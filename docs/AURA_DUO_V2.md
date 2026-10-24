# AURA DUO v2 — clearance and rendering correction

Based on colleague commit `cd83914`. The prior local D0 draft and preliminary edits are preserved in the Git stash named `Preserve local AURA DUO D0 and preliminary D1 before colleague update`.

## Geometry

The pushed v1 placed the pencil axis 37 mm from the ring center. Under a centered 84.1 mm-wide phone envelope, that puts the pencil over the phone edge. v2 moves the original sheath outward by 26 mm to a 63 mm axis offset and extends its connecting arm. The original sheath, bore, five magnet pockets, ring recess and right-side base region retain their nominal geometry. Hardware recesses are re-cut after the arm union to keep the bridge from plugging them; the boolean tools add 0.001 mm radial/depth relief to avoid coincident STL surfaces. The inherited bore actually measures 9.6 mm, despite the previous page calling it 8.9 mm; 8.9 mm is the reference barrel diameter.

With an assumed 1.5 mm case edge on each side:

- Sheath-to-case gap: 12.45 mm, measured from the reloaded STL's full-width sheath section.
- Pencil-to-case gap: 15 mm.
- Main part: 102.5 × 114.54 × 14.9 mm.
- Ring registration on the phone is illustrative; measure the selected case before printing for use.

The wider arm increases leverage on the base. Its strength, case attachment and pencil retention need physical testing. The ring notch does not by itself prove hinge sweep clearance.

## Assembly and images

All CAD scenes use one coordinate frame: X across the phone, Y along its long edge, Z normal to the back. The pen is built along Y, coaxial with the sheath. Only the camera rotates the completed assembly. Mesh-derived pen angles to the long edge and back plane are both 0°. The schematic pencil and holder do not intersect.

The 166 × 8.9 mm Pencil Pro envelope follows the colleague's mechanical-storage brief. This does not claim electronic writing support by the phone. The rendered device is a simplified envelope, not a detailed Apple CAD model. AI lifestyle images illustrate the intended arrangement; the CAD and dimensioned diagram are the geometry references.

## Rebuild and inspect

Run `.venv/bin/python scripts/aura_duo/build.py` from the repository root. Dependencies: numpy, trimesh, manifold3d and Pillow. The source input mesh is preserved at `scripts/aura_duo/input-v1.stl`.

The build exports `assets/stl/side/AURA_DUO_iPhone_v2.stl`, `AURA_DUO_v2_checks.json`, and revised part/closed/unfolded/back-view renders. Checks cover watertightness, consistent winding, positive volume, single-solid geometry, the unobstructed ring region and hardware pockets, sheath edge gap, mesh-derived axis alignment and pen/holder collision.

The page's catalog key stays `AURA_DUO_iPhone`; model paths and downloads point to v2. Old assets remain archived in Git but are no longer referenced on the product page.
