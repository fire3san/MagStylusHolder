# BOOX InkSense Plus holder — prototype v0.1

**Recommended starting point: B, the guarded diagonal cradle. Print fit samples before a full holder.** These are printable development prototypes, not a validated production product. The case dimensions, ring location, ring material/polarity and purchased hardware remain unknown. All STL units are millimetres; never scale the whole STL to fix a pen or magnet fit.

## What I would change in your sketches

I interpret design1.pdf as a round magnetic base with a short central pen holder, and design2.pdf as a similar base with an extended holder. Some handwritten dimensions are ambiguous; I have not treated them as manufacturing dimensions.

* **Keep the detachable ring interface.** It lets you remove the holder while reading. However, a round magnetic interface can rotate and peel off. Longer arms make peeling easier. Do not use the holder as a carrying handle.
* **Move pen retention to mechanical clips and soft bands.** N52 magnets should attach the holder to the case, not be relied on to retain this pen. Magnetic attraction of the stylus barrel has not been established.
* **Replace a long tight tunnel with two short clips.** A tunnel magnifies print errors, collects grit, requires axial insertion space and may catch the side button. Short clips allow top loading and easier cleaning. Their opening and force still need real testing.
* **Protect both ends, not only the nib.** A small puck leaves long unsupported ends that can snag or strike the floor. B adds end guards and an open cradle. It is not a sealed protective case or a guaranteed drop protector.
* **Rotate the pen diagonally.** The official pen is 157.5 mm long and the bare reader is 149 mm tall. A vertical pen protrudes 8.5 mm in total even before adding end guards. At 34 degrees from vertical, the nominal B assembly spans about 103.1 × 144.2 mm. This fits the bare reader's rectangular bounds only when centred; actual rounded corners and case ring position must be checked.
* **Reduce the magnetic base to an open annulus and spine.** The base is 3.2 mm thick, with 1.05–1.2 mm of plastic above the hardware cavities. A 5 mm solid plate is unnecessary for this prototype. The pen itself sets a practical lower bound on assembled thickness.

## Prototype choices

| Feature | A: compact clips | B: guarded cradle — recommended |
|---|---|---|
| Printed bounding size | 64 × 94 × 12.1 mm | 64 × 166.5 × 14.0 mm |
| Approximate nylon mass | 8–10 g | 15–17 g |
| Installed depth with nominal pen | 13.3 mm + interface film/pads | 14.0 mm + interface film/pads |
| Pen end protection | None | Open-top guards at both ends |
| Daily access | Snap out from top | Snap out from top |
| Travel retention | Soft bands required | Soft bands required |
| Main compromise | Exposed pen ends | Longer and heavier |

Mass is computed from solid mesh volume at assumed nylon density 1.01 g/cm³. It excludes magnets, glue, bands and surface finish. B is the better match for your concern about damage; A is useful for comparing comfort and convenience.

A third direction worth considering is a **soft sleeve on a thin ring plate**, with a fabric flap over the pen's end. It would avoid hard clips, feel better against your hand and absorb small knocks, but adds a sewn/bonded part and can retain grit. A fourth direction is an **edge-mounted holster**, which reduces the rear bump but needs your exact case geometry and increases the reader's width. Neither is represented as a finished STL in this package.

## Dimensions and assumptions

* Confirmed model: BOOX InkSense Plus. Manufacturer nominal dimensions: Ø9 × 157.5 mm; mass about 15.3 g. Bare Go 6 Gen II: 109 × 149 × 6.8 mm.
* Main clip bore: 9.4 mm, radial clearance 0.2 mm around a nominal 9 mm barrel. Print samples with 9.2, 9.4 and 9.6 mm bores. Main models use 9.4 mm until samples justify a change.
* Clip wall: 1.2 mm. Axial clip length: 8 mm. Mouth: 7.8 mm. Clip centres: ±40 mm along the spine. This is an experimental spring geometry, not a calculated fatigue life.
* Clip centreline above underside: 8.8 mm; nominal pen top: 13.3 mm. B's cradle floor is at 4.0 mm, below the nominal barrel bottom at 4.3 mm.
* B's inner end-to-end space: 163.5 mm. A centred 157.5 mm pen has 3 mm clearance at each end. The guards deliberately do not use the nib as a stop. There is no measured shoulder seat: if the pen slides, its nib can still reach an end wall. Tighten soft retention bands and verify axial retention before use.
* Side button, charging port and exact barrel profile have not been measured. Orient the side button upward and away from clips/bands; verify it is not depressed. Remove the pen for charging. Relocate clips parametrically if they interfere.
* Strap slots: 2 × 10 mm, two pairs. Use two approximately 8 mm wide, thin soft hook-and-loop straps or equivalent elastic closures. Underside strap relief is 0.8 mm deep. Thick straps may lift the magnetic interface and reduce attraction.

## Choose ONE hardware route

### Purchased magnetic ring assembly — preferred for a magnetic case

Use `*_ring_PROVISIONAL.stl`. Its underside recess is **58.4 mm OD × 47.6 mm ID × 2.0 mm deep**, provisionally accommodating an insert around **58 mm OD × 48 mm ID × 1.8 mm thick**, including any backing. These are chosen design assumptions, not a universal MagSafe dimension. Purchase an accessory-side magnetic assembly that is demonstrably attracted to your particular case; verify its geometry and polarity first. A passive steel ring is not a magnetic assembly. Two steel rings will not attract each other.

The radial clearances are 0.2 mm per side. Allow adhesive and protective-film thickness in the final stack. The model has no snap-in ring lid. Fix the insert with an adhesive suitable for its coating and nylon, following the adhesive supplier's preparation/cure directions. A thin bonded PET facing film over the cavity can help retain hardware and prevent rubbing; its bond must be tested. Hardware cannot be considered safely retained by a loose fit alone.

### Twelve N52 discs — experimental route for a STEEL case ring

Use `*_discs_PROVISIONAL.stl`. It has **12 pockets, Ø5.3 × 2.15 mm deep, on a 54 mm pitch circle**, for axially magnetized **Ø5 × 2 mm** discs. Minimum plastic roof is 1.05 mm. The nominal discs span radii 24.5–29.5 mm; your steel ring needs suitable overlap at those radii. A narrow or differently sized ring may give poor contact.

N52 describes the magnet material grade, not the installed holding force. Thin steel, small contact area, gaps, glue, film, peeling and sideways loads all matter. Do not infer a load rating from the grade or add up catalogue pull figures. Random disc placement against a multipole magnetic case can give mixed attraction and repulsion; the disc model is **not verified as MagSafe-compatible**.

Test the mating attraction and layout before bonding. For a steel mating ring, use a consistent marked assembly orientation and document it for repeatability. Bond each disc and retain the exposed side with a bonded film. Do not press oversized magnets into the nylon. Keep loose magnets away from the reader during assembly.

## Print sequence

1. Ask the shop for **SLS or MJF unfilled PA12 nylon**, cleaned and lightly deburred. This is the baseline for every clip and the full holder. Avoid generic brittle SLA resin for repeated clip flexing. PA11 can be considered for a later flex comparison, but do not assume it will have the same retention force.
2. First print the three `fit_clip` pieces and only the hardware fit sample for your chosen route. Each clip sample is separate; ask the shop to label the bags 9.2, 9.4 and 9.6. No engraving is built into these small samples.
3. Test with a smooth 9 mm dummy rod first. Then gently try the actual pen over a towel. Stop if force is excessive or the barrel marks. Choose the lightest reliable fit. The clearance samples do not replace a mouth-width/flex redesign if all three are too stiff.
4. Confirm the case measurements and purchased hardware. Use `placement-template.svg`, printed at actual size with its 100 mm scale checked, to test the proposed diagonal location. The template's case corner radius is illustrative.
5. Print **one B model for the selected hardware route**, after applying any dimensional changes. A is optional for comparison. Do not order all four full holders by default.
6. The STLs are in assembly coordinates with the case face at Z=0. Let the SLS/MJF shop choose packing orientation and compensate using its calibrated process. Ask it to preserve the functional sizes. Clip contacts and slot edges must be smooth. Do not coat or aggressively polish fit surfaces.

For an FDM-only shop, use the models for rough fit exploration only until clip orientation, layer adhesion, supports and material are redesigned/tested. Standard PLA or a pretty resin print should not be substituted for the functional nylon print without discussion.

## Assembly and retention checks

Install and fully cure the selected hardware. Add thin, grippy pads on the nonmagnetic portions of the underside if needed, keeping pad stand-off low enough for reliable attraction. They may resist rotation but are not a mechanical rotation lock. Feed a soft strap through each slot pair, with the underside run in the shallow recess and the closure above the pen. Do not clamp the side button. Set pen-end clearances before closing both straps.

Because a magnetic accessory can detach, add a short soft tether from one spare slot to an **independent secure case anchor**, if available. Do not tie it only to the same ring or to the nib. If the case has no suitable anchor, this prototype has no independent backup against complete magnetic detachment; a case-specific hook is a future revision requiring measurements.

Suggested prototype acceptance checks, not certified limits:

* Inspect every clip for roughness, cracks and whitening. Perform 100 insertion/removal cycles with a dummy rod before using the real pen; recheck retention and surface damage. This is a screening test, not a durability guarantee.
* With travel straps closed, apply an axial pull of about 3 N to the dummy pen for 10 seconds in each direction. Reject any slide that reduces the nib clearance. Adjust straps/liner or redesign as necessary.
* On the actual case with the reader removed, test at least 5 N of lateral force at the holder and 0.1 N·m of twisting moment, checking that the case ring itself does not peel. These are initial engineering targets, not predicted holding capability. With an approximately 45 g pen-plus-holder assembly, 10 g acceleration corresponds to roughly 4.4 N; a floor impact can exceed this substantially.
* Open the clips while holding the base. If pen removal lifts or peels the magnetic base off the case, clip force exceeds the useful attachment margin; redesign the clip or improve the interface.
* Shake in a padded bag with a dummy pen and dummy reader mass. Progress to a 0.3 m padded drop only with dummies. Check for pen escape, nib contact, magnet loss, rotation and cracks. Do not start drop testing with the BOOX or stylus.
* With the reader installed, check sleep/wake, touch and writing with the holder attached, detached and rotated. Additional magnets may affect cover sensing; compatibility has not been tested. Check that the folio can close and that its folded cover does not block the ring.

## What has been checked digitally

All nine exported STL files were reopened and checked for watertightness, consistent winding, positive volume and one connected solid. Both main designs have zero Boolean collision with a nominal Ø9 × 157.5 mm cylindrical pen at the intended centreline. See `mesh_checks.json` and `assembly_checks.json`. These checks do not validate forces, fatigue, print tolerances, magnetic performance, button clearance, case fit or drop protection. `model-preview.png` is rendered from the exported meshes.

The editable source is `source/build_models.py` (Python, manifold3d, trimesh, numpy). Change named parameters and rebuild to change fit; update the associated placement template and assembly checks if lengths or position change. No STEP solid or manufacturing certification is included.

## Measurements needed before a final full-size order

Case outer width and height; ring OD/ID/thickness; whether the case ring is steel or magnetic; ring centre measured from the case's left and top edges; any raised texture or fold-back-cover obstruction. Also confirm the magnetic insert's full dimensions including backing/adhesive, and the button's distance from the pen end. A straight-on case-back photo with a ruler is useful in addition to measurements.

## Sources

Accessed 19 October 2026. Published sizes are nominal; your parts remain the final fit reference.

* [BOOX InkSense Plus specifications](https://shop.boox.com/products/boox-inksense-plus-stylus): pen size, mass and button/charging features.
* [BOOX Go 6 Gen II specifications](https://shop.boox.com/products/go6gen2): bare reader size and compatible stylus.
* [K&J Magnetics: testing magnet strength](https://www.kjmagnetics.com/blog/testing-magnet-strength): dependence on mating steel and gaps.
* [K&J Magnetics: shear force](https://www.kjmagnetics.com/blog/magnet-shear-force): sideways loading differs from normal pull.
* [Formlabs SLS design guide](https://formlabs.com/white-papers/fuse-series-sls-design-guide/): process-specific fit and design considerations. The prototype dimensions and test targets above are engineering starting assumptions, not values certified by these sources.
