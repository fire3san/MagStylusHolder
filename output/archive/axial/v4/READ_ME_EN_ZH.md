# v4 — corrected K+M and one-tunnel scabbard

These replace the interpretation in v3, not the existing files. Both designs have **no strap slots or strap hardware**. Each main STL is a single connected printed body. The purchased magnets and bonded retaining spacers are installed afterward.

## K+M

`KM_fused_collar_under_magnets.stl`: approximately 68 × 68 × 16.3 mm. The old orange collar silhouette (11.4 mm body diameter, 14 mm central flange, 12 mm length, narrow 1.6 mm top split) is now fused into the central support. It is the same printed material as the base, not a separate soft TPU part. The two small end clips remain.

The rigid collar bore is changed to **9.4 mm**, rather than copying the old interference-fit TPU bore. This prevents treating a flexible part's fit as suitable for rigid nylon. It needs **axial insertion**, because the narrow split is not designed to spread over a 9 mm pen. Do not force the pen through the top. Verify the side button passes through the bore using the included sample first.

Three Ø6.3 mm sockets load from underneath at Y=-12, 0 and +12, under the centre spine/collar region. The socket ceiling is at Z=4.0; the collar bore floor is Z=4.6, leaving 0.6 mm plastic. Nominal pen bottom is Z=4.8: magnet-to-pen separation is approximately **0.8 mm**, before actual print/fit variation. Magnets are hidden underneath, not mounted visibly on top.

Fusing the collar into the base removes the old collar/dock axial keying function: the pen can slide through this fixed collar. This is not a positive axial latch. With the strap removed, reliable retention depends on actual fit and verified magnetic attraction. Do not assume the pen barrel attracts at all three selected locations.

## Rounded scabbard

`S_single_tunnel_rounded.stl`: approximately 68 × 128 × 16 mm. A single continuous 9.6 mm bore replaces the two disconnected tunnels. The exterior has a domed closed nose, a capsule-shaped base outline with rounded edge transitions, softened support edges and a short conical entrance lead-in. There is no separate upper guide ring, strap slot or long open channel.

The bore terminates at Y=-80 and opens at approximately +38. With the nominal pen centred at Y=0, tip clearance is only 1.25 mm. For a starting bench position, move the pen about 2.5 mm toward the entrance, giving approximately 3.75 mm tip clearance, and mark this insertion depth. There is **no measured barrel-shoulder stop**: the nib must not be used as an end stop, and the pen could slide toward it. Magnetic retention is untested.

Three underside sockets sit at Y=-68, -54 and -40. Here the bore floor is Z=5.0 and socket ceiling Z=4.0, so the separating roof is 1.0 mm. Nominal pen bottom is Z=5.3: magnet-to-pen separation approximately **1.3 mm**. This increased gap can reduce attraction compared with earlier top-pocket designs. The longer tunnel also makes side-button clearance and powder removal more important. Test the sample before ordering the full body.

## Common assembly

Each socket is Ø6.3 × 4.0 mm deep. Install one purchased **Ø6 × 2 mm axially magnetized N52 disc** against its ceiling, with the experimentally confirmed attracting face toward the pen. Add a **Ø6.05 × 1.9 mm printed spacer** behind it and bond it in place; approximately 0.1 mm remains for the bond stack. Print `magnet_spacer_6.05x1.9_print_3_per_holder.stl` three times per holder. These are retaining spacers, not press-fit plugs. Do not reuse the taller v3 spacers. Use a thin bonded protective facing over the underside and verify all hardware is secure. Adhesive choice and surface preparation must suit nylon and the magnet coating. Never force a magnet against the thin roof.

The case-attachment ring is separate hardware in the large underside recess: **58.4 OD / 39.6 ID / 2.0 deep**, still provisional for roughly 58/40/1.8 mm hardware. Confirm the actual case ring dimensions, material and polarity before bonding. Two passive steel rings will not attract. The small pen magnets do not replace the case-attachment ring.

## Print and test

Use unfilled SLS/MJF PA12 for these rigid bodies. Ask the shop to confirm its ability to produce the 0.6 mm K+M socket roof. Print the two bore/socket samples first, plus spacers. Smooth contact edges and clear all powder; do not coat the bores heavily. Do not scale an entire STL to change fit. Neither sample duplicates the full holder's insertion friction, but each checks local bore, button passage and socket stack.

Test with a smooth 9 mm dummy rod before the pen. Then test actual magnetic attraction at the intended gap and pen location, each magnet orientation separately. Suggested prototype screen: apply an axial load of approximately 3 N for 10 seconds in each direction, and reject more than 1 mm of slip; these are chosen screening targets, not certified limits. Check no movement toward the scabbard end wall, then perform repeated insertion/removal and padded bag-shake tests with dummy hardware. If either fails, treat it as a shape/fit prototype and revise retention; do not assume stronger magnets alone will solve it. No strap is included or required by this design brief.

All five exported meshes passed watertightness, winding, volume and connected-solid checks. Both main bodies clear a nominal 9 × 157.5 mm cylindrical pen at the intended position and sampled axial insertion positions. Magnet volumes also clear the sockets. Real button geometry, taper, force, fatigue, adhesion and drop behaviour are unverified. Editable source and `checks.json` are included. Prior versions are unchanged.

---

# 淘宝打印与装配说明

本次v4两款主体均**取消绑带槽**，主体各自一体打印。K+M中央原橙色笔圈形状已与底座融合，不再单独打印TPU笔圈；三个笔用磁铁孔位于背面。笔圈内径改为9.4 mm，须沿轴向穿笔，不能从1.6 mm窄缝硬掰塞入。

笔鞘为**单根连续9.6 mm内径管**，前端封闭圆头、底轨胶囊形圆边、入口带短导入斜面，没有第二导向环。总包络约68 × 128 ×16 mm。内部没有实测笔肩止挡，笔尖不得顶到底。

先各打印1个 `KM_bore_and_socket_sample.stl`、`S_bore_and_socket_sample.stl`，再确认侧键通行与磁吸效果。主体及配合件用非填充PA12 SLS/MJF。K+M磁铁孔顶壁0.6 mm，请店家先确认可加工性。清除管内全部粉末，轻去毛刺，不厚喷漆。

每主体需3个Ø6 ×2 mm N52磁铁，背面孔Ø6.3 ×4.0深。磁铁先顶到孔顶，再装Ø6.05 ×1.9 mm胶粘垫柱；`magnet_spacer_6.05x1.9_print_3_per_holder.stl` 每主体打印3件，留胶余量约0.1 mm，最后加薄覆膜固定。不能用v3的高垫柱，不是强压配合。磁极先用真笔确认，店家不要擅自装极性。

底部大磁环槽58.4/39.6/2.0 mm仍待实物确认，与三个笔用磁铁孔用途不同。K+M磁铁到名义笔杆间距约0.8 mm，笔鞘约1.3 mm，吸力需实测。无绑带也无轴向锁扣，不能承诺防滑或防摔。主体按毫米100%打印，不可整体缩放。
