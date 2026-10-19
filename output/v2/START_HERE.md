# Compact BOOX holder: v2 comparison pack

## Recommendation

Print small test pieces first, then compare **M (magnet-assisted)** with **K (keyed soft collar)**. Both have a 68 mm puck footprint. Neither has a long rail or end guard. The pen ends remain exposed. These are mechanically checked development prototypes, not validated products or guaranteed drop protection.

The red-circled slots in your screenshot are **strap slots**. A thin soft strap passes up through one slot, over the pen, down through the other slot, and closes on itself. They are not magnet pockets. The screenshot shows the earlier two-ended holder; the supplied colleague STL is a different, round puck with a closed pen tunnel.

## Review of the colleague STL

Inspected file: `boox_puck_N52_6x2mm_CLEAN_MANIFOLD.stl`. It has a watertight, consistently wound, connected solid, with 2,236 triangles and positive volume. This means the mesh is structurally valid for slicing, not that the design works in use.

Measured/reconstructed from mesh sections (approximately, millimetres):

| Feature | Finding | Consequence |
|---|---|---|
| Overall size | 68 × 68 × 16.80 | Compact footprint, relatively thick |
| Closed pen tunnel | Bore 10.4; outer diameter 17; enclosed length 44 | 9 mm pen has 1.4 mm diametral clearance; no axial stop |
| Pen bore centre | Original Z=7 | Lowest bore surface at Z=1.8 |
| Pen magnet pockets | Three Ø6.6 bores at X=-11, 0, +11; pocket floor at Z≈-0.2001 | Intended for Ø6 × 2 discs; nominal magnet tops reach bore bottom at Z≈1.8 |
| Magnet loading | Open into pen tunnel, closed underneath | Install through tunnel ends using a positioning tool; centre pocket is awkward to reach |
| Case attachment recess | Approximately Ø58 outer / Ø40 inner, 3.7 deep | Requires a separate matching ring assembly; dimensions and polarity unverified |
| Printed volume | 22.40 cm³ | About 22.6 g at assumed PA12 density 1.01 g/cm³, excluding hardware |

**Verdict: geometrically printable, but not ready to trust for transport.** The closed tunnel prevents the pen escaping sideways, but allows it to slide lengthwise. The three magnets help only if they attract the corresponding region and orientation of your actual pen sufficiently. The official pen specifications do not give a retention force or a magnetic attachment layout. N52 does not establish either. The tunnel can also catch the side button during insertion, depending on its protrusion and orientation.

The pockets are not missing or sealed: they are accessed from inside the tunnel. I retained the compact puck idea, but reconstructed the functional geometry to improve access, weight and retention. The original STL is untouched.

The original ring groove also needs a thickness check: a 1.8 mm thick insert seated at the back of a 3.7 mm deep groove would sit about 1.9 mm behind the underside plane before adhesive. Such stand-off can weaken attraction. Do not assume a ring fits just because its diameters match.

## Two prototypes to compare

| | M: magnet-assisted | K: keyed soft collar |
|---|---|---|
| Main file | `M_compact_puck_PA12.stl` | `K_compact_puck_PA12.stl` |
| Printed body | Ø68 × 12.6 high | Ø68 × 12.6 high |
| Nominal assembled depth | 13.8 with pen | 16.3 with pen/collar |
| Pen magnets | Three optional Ø6 × 2 N52 discs | None needed |
| Pen insertion | Press down into two short clips | Fit collar to pen, locate flange, press down |
| Axial retention | Strap friction plus any verified magnetic attraction | Collar flange meets groove shoulders; collar grip holds pen |
| Travel closure | One soft 8 mm strap | One soft 8 mm strap, essential to hold collar down |
| Main limitation | Magnetic grip unknown; still friction-dependent | Collar-to-pen friction and fatigue untested; extra part stays on pen |

Both depths exclude strap thickness, case magnet facing film, padding and adhesive. Their nylon bodies use approximately 8.4–9.0 cm³ of material (about 8.5–9.1 g at assumed density). See `mesh_checks.json` for exact generated volume. TPU density is not assumed; collar mass is not included.

K has a **locating feature**, not an infallible positive lock to the pen. Its flange is mechanically blocked from moving along the dock, but the collar can slip on the barrel or lift out if the strap is open. No claim of slip-proof or drop-proof performance is made.

## Magnet placement — M

There are two separate magnetic interfaces:

1. **Pen magnets:** three small round pockets on top, between the clips, at Y=-12, 0 and +12. Each pocket is Ø6.3, 2.2 mm deep. Install a Ø6 × 2 disc with the circular face pointing toward the pen. Pocket floor Z=2.4; magnet top Z=4.4 before adhesive. The nominal 9 mm barrel bottom is Z=4.8, leaving 0.4 mm before accounting for glue, film, tolerances and pen movement within the clip.
2. **Case attachment:** the large annular recess underneath. It is for a separate case-matching ring assembly. The small top magnets are not a substitute for this ring.

Start by placing the pen on a towel. With one magnet safely held in a temporary nonmetallic holder, map attraction along the barrel and around its circumference. Check both magnet faces. Do not let a loose magnet strike the pen. Do not assume all barrel regions attract equally or all three pockets need magnets. Mark useful positions and the face that attracts at each position. If useful attraction is only near one end, the fixed central three-pocket layout may not help; change pocket locations after measuring rather than committing to adhesive.

Use `magnet_test_6x2_PA12.stl` to test the three positions before building the complete M assembly. Secure magnets with removable film for the bench test; do not carry loose magnets. A thin protective layer must prevent direct metal-to-pen rubbing. For the final prototype, bond each magnet with a coating-compatible adhesive, then cover the pocket openings with a durable thin bonded film. Verify the actual stack does not touch or scratch the pen. No printed magnet lid is supplied.

Test attraction at the intended installed gap, not only with the magnet touching the barrel. Compare M with the same clips and strap with/without magnets. If attraction is weak, omit the magnets and use K; do not keep adding stronger magnets blindly.

On the flat test block, two 0.2 mm shims at its ends raise the barrel bottom from the 4.6 mm block surface to 4.8 mm, approximating the main holder's 0.4 mm magnet-to-barrel gap. Recheck with your actual adhesive and protective film; they change the stack. Do not infer final force from an unshimmed direct-contact test.

## Collar placement — K

The supplied split TPU collar has a 12 mm axial length, 11.4 mm body diameter, and a 14 mm diameter × 3 mm wide central flange. The dock groove is 3.6 mm wide, giving 0.6 mm total nominal axial play. A 1 mm rigid shift of the assembled collar causes CAD interference at the shoulder, confirming the locating function. Real TPU can deform, so this is not a load test.

Print the three collar bores in **flexible TPU**, not nylon or ordinary resin:

* 9.0 mm: zero nominal interference; begin here for gentle fit.
* 8.8 mm: 0.2 mm diametral interference, suggested comparison size.
* 8.6 mm: 0.4 mm interference, only if the softer/larger samples slide too easily.

The 1.6 mm longitudinal split allows the collar to spread around the barrel. Begin on a smooth 9 mm dummy rod. Do not force a stiff collar over the real pen. Aim the split upward, seat the flange in the central groove, and close an approximately 8 mm wide soft hook-and-loop strap through the slots over the collar. The groove is below the pen, not a magnet pocket. The minimum nominal web between the key groove and underside strap recess is 1.25 mm.

Position the collar on a constant-diameter barrel region clear of the button, charging port and normal writing grip. If leaving it on the pen feels uncomfortable, that is a real reason to prefer M or revise the collar position/length. Do not bond the collar to the pen as part of this first test.

## Common case interface and assembly

The underside recess is **58.4 OD × 39.6 ID × 2.0 deep**, provisionally for a ring assembly approximately **58 OD × 40 ID × 1.8 thick**, allowing adhesive. This follows the colleague model's approximate ring footprint but changes its depth and adds clearance. It is **different from the v1 pack's 48 mm ID ring**: do not mix hardware between versions.

Confirm the actual ring before printing the full puck. If the case has only a steel ring, the holder needs magnets. If the case already has magnets, select a genuinely attracting accessory-side ring or suitable steel counterpart. Two steel rings will not attract. A magnetic ring's polarity pattern is not established by its dimensions or by the word MagSafe.

The base is 3.2 mm; the ring recess leaves a 1.2 mm roof. Bond the ring and use a suitable thin protective facing film. Strap recess underneath is 0.8 mm deep; a thicker strap may lift the mount and weaken attraction. Low-profile grip pads may resist rotation but do not mechanically lock it. A short soft tether to an independent case anchor can back up magnetic detachment if your case provides an anchor. Neither prototype includes a case-specific latch.

## Printing and A/B test

**Stage 1:** Print three PA12 clip samples, the magnet test block, and three TPU collars. Print the case-ring sample only once the actual ring has been measured. Clip bores are 9.2/9.4/9.6; clip walls 1.2; opening 7.8; contact length 7. Main models use 9.4 until samples indicate otherwise. Do not scale whole STLs to change fit.

**Stage 2:** Print one M and one K body in unfilled SLS/MJF PA12, using the same process as the clip coupons. Rebuild if a different clip size is chosen. For collars, request flexible TPU around Shore 90A–95A and disclose the 1.2 mm nominal body wall; ask the shop to confirm manufacturability and dimensional capability. FDM TPU with the supplied vertical-axis orientation is a practical collar trial if SLS TPU minimum-wall limits prevent reliable printing. Keep the same TPU material/process across comparison sizes. Do not assume different TPU brands give the same grip.

**Stage 3:** Assemble and compare over a towel. The following are prototype screening targets, not certified standards:

* Inspect and deburr all pen-contact edges. Check button and charging-port clearance.
* Use a dummy rod for 100 insertion/removal cycles. Reject cracks, whitening or lost retention.
* With strap closed, pull the dummy rod axially in each direction at approximately 3 N for 10 seconds. Record slip; target no more than 1 mm. For K, mark pen/collar and collar/dock separately to identify which interface moves.
* Compare M with and without magnets, keeping the strap and clip fit unchanged. Record ease of removal and axial slip. Test multiple pen orientations only after confirming no scratching or button loading.
* On an empty case with a dummy payload, screen the ring attachment with about 5 N lateral load and 0.1 N·m twist. Reject rotation, ring peeling, loose magnets or detachment. These forces are chosen test targets, not predicted capacity.
* Check bag snagging and shake retention with dummy hardware. These compact pucks do not protect exposed pen ends in a floor impact. Do not drop the actual BOOX to test them.
* Check sleep/wake, touch and writing with all magnets fitted. New magnets may affect cover sensing. This has not been verified on your device.

Record material, collar bore, clip bore, strap thickness, magnet positions/polarity and results in `TEST_RECORD.csv`. Choose the design from these tests, not from the render alone.

## Digital checks and remaining uncertainty

All 10 exported STLs were reopened and checked for watertightness, consistent winding, positive volume and one connected solid. Both docks clear a nominal Ø9 × 157.5 cylindrical pen. K clears the undeformed 8.8 mm collar and has the intended locating interference after axial displacement. Collar/pen interference is intentional for a soft part and is not a fit prediction. No finite-element, fatigue, magnetic-force, actual-pen or drop testing has been performed.

Original model sections: `colleague_sections.json`. New checks: `mesh_checks.json` and `assembly_checks.json`. Editable geometry: `source/build_v2.py`. The assembled/exploded illustration is generated from the CAD geometry; the purple strap route is schematic. No strap, magnets, adhesive or case ring are supplied by the STLs.

Still needed for finalisation: case ring dimensions and material/polarity; its centre position; actual pen magnetic response; side-button position/height; and results from the first fit print.

Reference specifications: [BOOX InkSense Plus](https://shop.boox.com/products/boox-inksense-plus-stylus). Flexible material context: [Formlabs TPU 90A](https://formlabs.com/products/tpu-90a-powder/). These do not validate this holder design. Accessed 19 October 2026.
