"""Correct the pushed AURA DUO v1, preserving its ring interface and sheath.
Run with .venv/bin/python scripts/aura_duo/build.py. Units: millimetres.
X crosses the phone, Y follows its long edge, Z points out of its back.
"""
from pathlib import Path
import json, math
import numpy as np
import trimesh
import manifold3d as mf
from PIL import ImageDraw, ImageFont
from render_common import render
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets/stl/side'
RENDERS=ROOT/'assets/renders/side'
PHONE_W=84.1; PHONE_H=117.8; CASE_EDGE=1.5
OLD_X=-37.; PEN_X=-53.55; PEN_Z=8.6; PEN_D=8.9; PEN_LEN=166.
BASE_T=3.4

def box(size,center): return mf.Manifold.cube(size,True).translate(center)
def cylinder(r,h,at=(0,0,0)): return mf.Manifold.cylinder(h,r,circular_segments=96).translate(at)
def solid_mesh(s):
 q=s.to_mesh()
 return trimesh.Trimesh(np.asarray(q.vert_properties)[:,:3],np.asarray(q.tri_verts),process=True)
def import_solid(t):
 s=mf.Manifold(mf.Mesh(np.asarray(t.vertices,dtype=np.float32),np.asarray(t.faces,dtype=np.uint32)))
 assert s.status()==mf.Error.NoError
 return s

original=trimesh.load_mesh(Path(__file__).with_name('input-v1.stl'))
source=import_solid(original)
# Extract the complete original sheath at its tangent to the base. Do not scale
# it: scaling would also change its bore, walls and five magnet pockets.
sheath=source ^ box((200,200,100),(-130,-88,0))  # x<=-30, y<=12
sheath=sheath.translate((PEN_X-OLD_X,0,0))
# Preserve the ring and its existing right-side notch; restore the small outer
# crescent cut off by the extraction plane before joining the longer arm.
base=source ^ box((200,250,100),(70,0,0))  # x>=-30
outer=cylinder(32.5,BASE_T)-cylinder(17.5,BASE_T+2,(0,0,-1))
recess=cylinder(29.2,2.01,(0,0,-.01))-cylinder(19.8,4,(0,0,-1))
crescent=(outer-recess) ^ box((200,250,100),(-130,0,0))
base+=crescent
bridge=mf.CrossSection([[(PEN_X-6,-10),(-21,-14),(-21,14),(PEN_X-6,10)]]).extrude(BASE_T)
# Cut hardware wells after all unions: the longer bridge must not fill them.
fixed=base+bridge+sheath
ring_tool=cylinder(29.201,2.011,(0,0,-.01))-cylinder(19.799,4,(0,0,-1))
fixed-=ring_tool
for pocket_y in [-12,-24,-36,-48,-60]:
 fixed-=cylinder(2.651,3.011,(PEN_X,pocket_y,-.01))
 assert (fixed ^ cylinder(2.5,1.,(PEN_X,pocket_y,1.8))).volume()<1e-5
assert (fixed ^ recess).volume()<1e-5
fixed=fixed.simplify(.0001)
assert fixed.status()==mf.Error.NoError and len(fixed.decompose())==1
path=OUT/'AURA_DUO_iPhone_v3.stl'
solid_mesh(fixed).export(path)
part=trimesh.load_mesh(path)
assert part.is_watertight and part.is_winding_consistent and part.volume>0
# The unchanged ring region must agree with the pushed source outside the arm.
ring_keep=box((100,100,30),(30,10,10)) # x>=-20; beyond the new bridge
assert ((fixed ^ ring_keep) - (source ^ ring_keep)).volume()<1e-3
# Check the unscaled sheath at its upper entry away from the new bridge.
upper=part.vertices[(part.vertices[:,0]<PEN_X+8)&(part.vertices[:,1]>5)]
sheath_inner_x=float(upper[:,0].max())
case_left=-(PHONE_W/2+CASE_EDGE)
case_gap=case_left-sheath_inner_x
assert 2.99 <= case_gap <= 3.01

# A schematic 166 mm, 8.9 mm Pencil Pro is retained from the colleague's brief.
# This describes mechanical storage only, not electronic support by the phone.
TIP_Y=-63.; TIP_LEN=10.
def y_cylinder(r,length,start):
 return cylinder(r,length).rotate((-90,0,0)).translate((PEN_X,start,PEN_Z))
pen_body=y_cylinder(PEN_D/2,PEN_LEN-TIP_LEN,TIP_Y+TIP_LEN)
pen_tip=mf.Manifold.cylinder(TIP_LEN,.2,PEN_D/2,circular_segments=96).rotate((-90,0,0)).translate((PEN_X,TIP_Y,PEN_Z))
pen_solid=pen_body+pen_tip
pen=solid_mesh(pen_solid)
_,_,axes=np.linalg.svd(pen.vertices-pen.vertices.mean(axis=0),full_matrices=False)
axis=axes[0]/np.linalg.norm(axes[0])
long_angle=math.degrees(math.acos(float(np.clip(abs(axis[1]),0,1))))
plane_angle=math.degrees(math.asin(float(np.clip(abs(axis[2]),0,1))))
assert long_angle<.01 and plane_angle<.01
assert (fixed ^ pen_solid).volume()<1e-3
# Reuse the existing bore and sockets; verify the intended pencil remains inside
# their axis rather than being rotated upright (along Z) in a separate render.
checks={'revision':'v3 / clearance and assembly correction','source_commit':'cd83914',
'watertight':bool(part.is_watertight),'consistent_winding':bool(part.is_winding_consistent),
'connected_solids':len(fixed.decompose()),'extents_mm':part.extents.round(3).tolist(),
'previous_pen_axis_offset_mm':63,'pen_axis_offset_mm':abs(PEN_X),
'phone_closed_width_mm':PHONE_W,'assumed_case_edge_mm':CASE_EDGE,
'sheath_to_case_gap_mm':round(case_gap,3),'pencil_to_case_gap_mm':round(abs(PEN_X)-PEN_D/2-(PHONE_W/2+CASE_EDGE),3),
'pen_axis_vs_phone_long_edge_deg':round(long_angle,6),'pen_axis_vs_back_plane_deg':round(plane_angle,6),
'pen_holder_collision_mm3':round((fixed ^ pen_solid).volume(),6),
'magnet_pockets_clear':True,'ring_recess_clear':True,'physical_fit_verified':False,'hinge_sweep_verified':False}
(OUT/'AURA_DUO_v3_checks.json').write_text(json.dumps(checks,indent=2)+'\n')

# Every part stays in the same assembly coordinates. Only the camera changes.
# Registration is illustrative; no camera/button shapes are invented.
closed_phone=solid_mesh(box((PHONE_W,PHONE_H,11.3),(0,0,-6.65)))
case=solid_mesh(box((PHONE_W+2*CASE_EDGE,PHONE_H+2*CASE_EDGE,1),(0,0,-.5)))
# Second half is across the hinge from the magnet-bearing back panel.
other=solid_mesh(box((80.5,PHONE_H,5.2),(PHONE_W/2+40.25+1.5,0,-3.6)))
# 68.88 mm ring height places the existing lower sheath at the bottom edge.
# Shift the device down relative to the ring to provide this nominal placement.
device_y=-10.
center=np.array([18.,10.,0.])
common=[(part.triangles,(53,84,90)),(pen.triangles,(232,230,218))]
closed=[(closed_phone.triangles+[0,device_y,0],(88,101,104)),(case.triangles+[0,device_y,0],(178,188,178))]+common
opened=closed+[(other.triangles+[0,device_y,0],(112,126,125))]
def scene(objects,w,h,scale,rx,rz,shift=center):
 return render([(tri-shift,color) for tri,color in objects],w=w,h=h,scale=scale,rx=rx,rz=rz)
# Dedicated part view remains holder-only for the viewer's studio tab.
part_center=(part.bounds[0]+part.bounds[1])/2
scene([(part.triangles,(53,84,90))],1200,1100,6,-48,-20,part_center).save(RENDERS/'AURA_DUO_v3_part.png')
scene(opened,1400,1200,5,-30,-12).save(RENDERS/'AURA_DUO_v3_unfolded.png')
scene(closed,1100,1200,5,-30,-12,np.array([-15.,10.,0.])).save(RENDERS/'AURA_DUO_v3_closed.png')
im=scene(opened,1400,1200,5,0,0)
d=ImageDraw.Draw(im);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',25)
d.text((50,40),'AURA DUO v3 / ORTHOGRAPHIC BACK VIEW',font=font,fill='#263a32')
d.text((50,82),f'Parallel pencil + phone axes / {case_gap:.2f} mm sheath-to-case gap*',font=font,fill='#52624f')
d.text((50,1130),'*1.5 mm case allowance; ring registration and fold sweep require measurement.',font=font,fill='#52624f')
im.save(RENDERS/'AURA_DUO_v3_back.png')
print(json.dumps(checks,indent=2))
