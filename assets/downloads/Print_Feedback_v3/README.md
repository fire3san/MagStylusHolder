# Print feedback revision / 2026-11-03

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
