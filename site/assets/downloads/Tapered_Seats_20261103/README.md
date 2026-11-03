# Tapered inner seats / 2026-11-03

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
