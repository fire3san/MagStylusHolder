# AURA DUO v3 / closer side storage

Rebuilt from the original colleague mesh with the same sheath, bore, ring and five clear magnet pockets. Pen axis moves inward from 63 to 53.55 mm. Under the 84.1 mm phone width and 1.5 mm case-edge assumption, sheath clearance is 3.00 mm and pen clearance 5.55 mm. Part envelope is 93.05 × 114.54 × 14.9 mm. Axis remains parallel to phone long edge and back plane. Watertight, single-solid, winding, hardware wells and pen collision checks pass. Physical case fit and hinge sweep remain unverified.

Rebuild: `.venv/bin/python scripts/aura_duo/build.py`. Outputs: `assets/stl/side/AURA_DUO_iPhone_v3.stl`, `AURA_DUO_v3_checks.json`, and v3 CAD renders. v2 remains historical.

# AERIS / measured overhang

Run `.venv/bin/python scripts/aeris-fit.py`. Actual STL bounds Y=-72..38 mm (110 mm). Centerline ray at X=0,Z=9.8 intersects the internal floor at Y=-61.96 mm. Keeping the specified 3 mm internal tip gap puts the tip at -58.96 and a 157.5 mm pen cap at +98.54.

Ring is 75 mm above case bottom: case bottom Y=-75. Sheath ends at -72, so the bottom gap is 3 mm. With a 149 mm device and provisional 1.5 mm case border at both ends: device bottom=-73.5, top=75.5; case top=77 and total case height=152. Cap protrudes 23.04 mm above the device, or 21.54 mm above that assumed case. Actual case height is not measured. General formula for cap above case: 173.54 minus measured case height. Earlier 24.54 mm assumed a 149 mm case envelope and is retained only as that historical assumption in the checks JSON. Neither current nor historical configuration fits the entire pen inside the device height.

The AERIS STL stays unchanged. The updated mounted CAD and lifestyle photo show the actual protruding pen. See `assets/story/aeris-fit-checks.json` and `assets/renders/v9/AERIS_fit_checked_back.png` for the dimensional reference.

ImageGen precise-object edit prompts: AURA DUO preserves the cafe/device scene and shifts the complete sheath/pencil inward 9.45 mm, shortening the bridge to leave a 3 mm edge gap. AERIS preserves the commuter scene but uses the measured CAD reference: 152 mm case, 110 mm sheath ending 3 mm above its bottom, 68 mm ring at 75 mm, 157.5 mm pen with its cap 21.54 mm above the case. Images remain concept illustrations.
