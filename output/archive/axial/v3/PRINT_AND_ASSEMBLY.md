# Three additional BOOX prototypes — v3

These supplement the v2 designs; they do not overwrite them. All dimensions are millimetres. All bodies are single connected printable solids. Hardware, straps and S magnet spacers are separate assembly items. Prototype fit and physical retention remain unverified.

## S: scabbard with three underside magnets

`S_scabbard_3magnets.stl`: 68 × 126 × 16 mm, printed volume 14.80 cm³ (about 14.95 g at assumed PA12 density 1.01 g/cm³, excluding hardware).

Interpretation of your marked image: remove the upper end guard; convert the upper clip into a closed entry guide; convert the lower clip/guard region into a blind-ended tunnel. The lower sheath is 56 mm long externally, and the upper guide 12 mm. The shorter 126 mm backbone replaces the previous 166.5 mm guarded design. It is still longer than the compact pucks.

The two bores are nominally 9.6 mm on a common axis at Z=9.8. Feed the pen nib-first through the upper guide and into the lower sleeve. The opening is not a snap clip. A smooth nominal 9 mm cylindrical pen has a clear insertion path. The real side button, taper and any protrusions have not been measured; test `tunnel_fit_ID9.6.stl` before printing the full S. Never force the button through the guide. If necessary increase the bore or add a button relief only after measuring the real pen.

With the 157.5 mm pen centred at Y=0, its nib end is at -78.75, while the sheath inner end is -82.4: **3.65 mm nominal tip clearance**. The bore does not contain a measured barrel-shoulder seat. The closed end is not an intended nib support: sliding can eliminate that clearance and strike the tip. Use the central soft strap for travel, mark insertion depth, and verify axial retention. The upper end of the pen remains exposed.

Three magnet sockets are underneath the lower sleeve at Y=-68, -54 and -40. Each is Ø6.3 × 4.4 deep. Install in this order, working from the underside:

1. Test and mark the attracting face against the corresponding actual pen region. Magnetise neither the pen nor any other part; use purchased axially magnetized Ø6 × 2 mm N52 discs. Useful attraction at these locations is not established.
2. Place each disc against the socket ceiling, with its tested attracting face toward the pen tunnel. Nominal disc position is Z=2.4 to 4.4.
3. Print `S_magnet_spacer_print_3.stl` **three times**. Each spacer is Ø6.05 × 2.3. Bond it behind its magnet. A nominal 0.1 mm remains for the bonding stack; verify actual dimensions and seating before curing. This is a glued spacer, not a press-fit or snap-fit lid.
4. Secure the underside with a thin, durable bonded facing film. No loose magnets or spacers should remain. The selected adhesive must suit the magnet coating and nylon; follow its supplier's preparation and cure directions.

There is a 0.6 mm plastic roof below the bore. Nominal magnet-to-pen surface separation is 0.9 mm (roof plus bore clearance), larger than MK2's nominal 0.4 mm gap. Consequently S may have less attraction for the same magnet and pen location. Test `S_socket_tunnel_test.stl` with a real magnet/spacer first. Do not force the magnet upward against this thin roof. Ask the print shop to confirm it can form and clean that feature reliably.

## K2: two integral retaining cuffs

`K2_integral_dual_cuffs.stl`: 68 × 68 × 12.57 mm body; nominal 13.8 mm depth with the pen, excluding straps/interface padding. Printed volume 8.83 cm³.

Both retaining cuffs are printed in the same PA12 body as the puck. Each is 12 mm long, with 9.2 mm nominal bore, 1.2 mm wall, and a 7.6 mm top opening. Centres are at Y=-23 and +23. Compared with v2's 7 mm clips, these have longer contact sections and slightly tighter nominal geometry. This may raise insertion force and friction; it is not a validated retention improvement until tested.

**These are integrated split cuffs, not the v2 keyed collar.** A keyed collar must move with the pen to engage a groove in the dock. Fusing it to the dock removes that action. Integrated cuffs restrain lateral escape but still rely on actual fit and strap friction against lengthwise sliding. Two full closed rings would require axial loading and button clearance, which S tests separately. The one-body versions use top loading for convenience.

Do not simply print the old soft collar geometry in rigid nylon or use an interference fit calculated for TPU. The main K2 bore has 0.2 mm nominal diametral clearance around a 9 mm barrel. Included 9.0/9.2/9.4 mm cuff samples explore tolerance and retention. They do not establish a safe insertion force or fatigue life. Print and test samples first. If all samples are too stiff, revise wall/opening geometry instead of forcing the pen.

## MK2: integral cuffs plus three pen magnets

`MK2_integral_dual_cuffs_3magnets.stl`: same 68 mm footprint, cuffs and nominal assembled depth as K2. Printed volume 8.91 cm³.

Three top-loading Ø6.3 × 2.2 mm deep pockets sit between the cuffs, at Y=-12, 0 and +12. Each takes a Ø6 × 2 disc; no S spacers are used here. With a disc seated on the Z=2.4 floor, its top is at 4.4 and the pen bottom at 4.8, before adhesive/film and fit variation. Use a thin protective bonded film over the pockets to keep metal from rubbing the pen and retain the magnets. Check the completed stack for clearance.

Test which pen regions and faces attract before bonding. These three positions may not align with an attractive region on your pen. If they do not, move the pockets parametrically or omit magnets; a stronger grade cannot compensate for a non-attracting barrel region. Keep the strap for travel even if the bench test feels strong.

## Common underside ring and strap

All three keep the v2 ring recess: **58.4 OD × 39.6 ID × 2.0 deep**, provisionally for approximately 58/40/1.8 mm hardware including its backing. This is not a universal MagSafe standard. Confirm size and mating polarity/material against the actual case. A steel ring on each side will not attract; an incompatible pair of magnetic rings can repel. The annular hardware connects the holder to the case; the small discs are for the pen.

The large ring recess needs its own bonded hardware and protective facing. Do not substitute the small pen magnets. The two central slots accept an approximately 8 mm wide soft strap routed over the pen, down through the other slot, and closed on itself. The underside strap relief is 0.8 mm deep. Keep the strap clear of the side button and account for any strap thickness that lifts the magnetic interface. These designs are not carrying handles. A short tether to an independent case anchor is useful if your case offers one.

## Print order and verification

1. Print the three `cuff_fit` pieces and `tunnel_fit_ID9.6`, plus `S_socket_tunnel_test` and one S spacer if testing S. All use unfilled SLS/MJF PA12. Do not substitute brittle general-purpose resin. A shop must approve its achievable tolerances and the 0.6 mm S roof.
2. Test a smooth dummy 9 mm rod first. Then check the real pen gently over a towel, including the side button. Select the least forceful reliable cuff size; main files use 9.2 until revised. Never scale the entire STL to change a bore.
3. After fit is confirmed, print the desired full prototypes. S needs three spacers; K2 and MK2 have no separate printed collar. Magnets/straps are purchased components. Use the same PA12 process as the samples. Clear all powder from the blind sleeve, smooth all pen-contact edges, and avoid thick coatings.
4. Screen cuff fatigue with 100 dummy-rod cycles. With the strap closed, test axial retention in each direction at approximately 3 N for 10 seconds; target no more than 1 mm slip. These are chosen prototype screening targets, not certified limits. For S, maintain the nib clearance throughout testing.
5. Compare K2 versus MK2 with the same strap and cuff fit. Test MK2 with and without magnets to separate the magnetic contribution. Check case-ring rotation/peeling on an empty case, and check device sleep/wake, touch and writing with the magnets installed. Real-world performance has not been tested.

Digital validation: all nine exported STL files were reopened and found watertight, consistently wound, positive-volume solids; the CAD objects each have one connected component. All three clear a nominal 9 × 157.5 mm cylindrical pen. S also clears axial insertion at sampled positions 10/30/60/100/160 mm above the final position. The nominal magnet volumes do not intersect the bodies. These checks exclude the real button, flex, magnet force, adhesion, fatigue and impacts. See `mesh_checks.json` and `assembly_checks.json`.

Editable source: `source/build_v3.py` and `source/geometry.py`; Python dependencies: manifold3d, trimesh, numpy. `render_v3.py` additionally uses Pillow. No STEP file, material certification or drop-performance claim is supplied. Earlier v1/v2 files are unchanged.
