# Supported tapered seats — 2026-11-03

All seven closed sheaths now have tapered internal support and a separate
relief pocket beneath the nib. This replaces the six flat bores and the
0.01 mm nominal nib clearance previously found in AURA SCREEN v3.

| Current model | Modeled nib-to-floor gap | Minimum new-seat wall |
| --- | ---: | ---: |
| AURA SCREEN v4 | 1.679 mm | 1.5 mm |
| AURA v4 | 1.679 mm | 1.5 mm |
| AURA DUO v4 | 1.675 mm | 1.5 mm |
| AURA DUO SCREEN v3 | 1.675 mm | 1.5 mm |
| AERIS v10 | 1.679 mm | 1.5 mm |
| VERTEX v10 | 1.679 mm | 1.5 mm |
| TITAN PRO v10 | 1.675 mm | 1.5 mm |

## Material thickness

Each new seat has at least 1.5 mm of surrounding material, including its end
and webs beside existing magnet pockets. A 1.55 mm spherical offset envelope
checks this in all directions, allowing 0.05 mm for tessellation/export
variation. The check runs again on the exported/reloaded STL. Seat depths are
selected individually to fit the available material.

This minimum applies to the new tip seat, not every pre-existing feature on
the whole part. Existing upper walls, slots, ring and magnet pockets remain.
External dimensions stay unchanged. AURA SCREEN retains its 10 mm shortening
and 2 mm inward move; other model lengths are unchanged.

## Nose support and nib relief

The taper supports an assumed 10 mm stylus nose. A narrow relief pocket extends
2 mm beyond its nominal end. At the modeled seated position, the nib has about
1.68 mm axial clearance. The wider nose meets the tapered sides before the nib
reaches the floor.

All seven exported STLs are watertight single solids. The build verifies no
intersection at the reference pen pose, clear upward extraction, and positive
nose-side contact under 0.1 mm downward overtravel while the nib stays clear.
Ring and upper-body preservation are also checked.

The barrel is assumed to be 9 mm for BOOX / 8.9 mm for the Pencil. These and
the 10 mm nose are assumptions, not measurements of the photographed stylus.
The CAD contact check does not establish force, fatigue, print strength or
physical retention. Actual pen geometry and print tolerances need a test print.

ORBIT and STRATOS retain protective cups with 3 mm modeled nib clearance.
Their clips/magnets provide retention. Open clips such as NEXUS and ECLIPSE do
not need a closed conical tip seat.

## Files and reproduction

- [Seven-model STL pack and individual cutaways](../../../assets/downloads/Tapered_Seats_20261103.zip)
- [Wall, contact, dimensions and hash checks](../../../assets/downloads/Tapered_Seats_20261103/checks.json)
- [Independent current-catalog measurements](../../../assets/reviews/tip-seats/checks.json)
- [All closed-sheath cutaways, with assumed pen in orange](../../../assets/reviews/tip-seats/all-sheath-sections.png)

```sh
.venv/bin/python scripts/build-tapered-seats.py
.venv/bin/python scripts/build-latest-pack.py
.venv/bin/python scripts/check-tip-seats.py
python3 scripts/sync-site.py
```

Old versioned packs remain available for comparison. The current product
catalog and latest six-model pack select the revised AURA SCREEN and AERIS.
