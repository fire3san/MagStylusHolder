"""Measure the current AERIS STL and render a dimensioned nominal assembly."""
from pathlib import Path
import sys,json
import numpy as np
import trimesh
import manifold3d as mf
from PIL import ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parent/'aura_duo'))
from render_common import render
ROOT=Path(__file__).resolve().parents[1]
m=trimesh.load_mesh(ROOT/'assets/stl/v9/S_Flow_BOOX_vertical.stl')
# Centerline ray through every triangle, independent of optional rtree packages.
o=np.array([0.,-100.,9.8]);d=np.array([0.,1.,0.]);v=m.triangles;e1=v[:,1]-v[:,0];e2=v[:,2]-v[:,0]
h=np.cross(np.broadcast_to(d,e2.shape),e2);a=np.einsum('ij,ij->i',e1,h);ok=abs(a)>1e-9
f=np.zeros_like(a);f[ok]=1/a[ok];s=o-v[:,0];u=f*np.einsum('ij,ij->i',s,h);q=np.cross(s,e1);vv=f*(q@d);t=f*np.einsum('ij,ij->i',e2,q)
hits=np.unique(np.round(-100+t[ok&(u>=0)&(vv>=0)&(u+vv<=1)&(t>=0)],6))
assert len(hits)==2
floor=float(hits[-1]);tip=floor+3.;cap=tip+157.5
case_bottom=-75.;case_edge=1.5;device_bottom=case_bottom+case_edge;device_top=device_bottom+149.;case_top=device_top+case_edge
checks={'holder_y_bounds_mm':m.bounds[:,1].tolist(),'centerline_internal_floor_y_mm':floor,'tip_internal_clearance_mm':3,'pen_length_mm':157.5,'pen_tip_y_mm':tip,'pen_cap_y_mm':cap,'ring_height_from_case_bottom_mm':75,'assumed_case_edge_mm':case_edge,'device_height_mm':149,'assumed_case_outer_height_mm':152,'sheath_bottom_to_case_bottom_mm':float(m.bounds[0,1]-case_bottom),'pen_overhang_above_bare_device_mm':round(cap-device_top,3),'pen_overhang_above_assumed_case_mm':round(cap-case_top,3),'legacy_149mm_case_envelope_overhang_mm':round(cap-(149-75),3),'physical_case_height_measured':False}
case=trimesh.creation.box((112,152,1.2));case.apply_translation((0,1,-.6))
phone=trimesh.creation.box((109,149,6.8));phone.apply_translation((0,1,-4.6))
body=trimesh.creation.cylinder(4.5,147.5,sections=64);body.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2,[1,0,0]));body.apply_translation((0,tip+10+147.5/2,9.8))
cone=trimesh.creation.cone(4.5,10,sections=64);cone.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]));cone.apply_translation((0,tip+10,9.8))
def solid(mesh):
 return mf.Manifold(mf.Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
collision=(solid(m) ^ (solid(body)+solid(cone))).volume()
assert collision < 1e-3, collision
checks['pen_holder_collision_mm3']=round(collision,6)
objects=[(phone.triangles,(100,111,105)),(case.triangles,(207,203,184)),(m.triangles,(53,107,101)),(body.triangles,(222,220,204)),(cone.triangles,(65,68,65))]
render(objects,w=1200,h=1200,scale=5.5,rx=-28,rz=-12).save(ROOT/'assets/renders/v9/AERIS_fit_checked_mounted.png')
im=render(objects,w=1200,h=1200,scale=4.8,rx=0,rz=0);dr=ImageDraw.Draw(im);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',24)
for y,line in [(30,'AERIS / measured STL + 157.5 mm reference pen'),(65,'149 mm reader + assumed 1.5 mm case edges = 152 mm case'),(1050,f'Case-bottom ring height 75 mm / sheath bottom gap 3 mm'),(1090,f'Pen cap above case {cap-case_top:.2f} mm / above device {cap-device_top:.2f} mm'),(1130,'Case height and pen fit still require physical measurement.')]:dr.text((35,y),line,font=font,fill='#263a32')
im.save(ROOT/'assets/renders/v9/AERIS_fit_checked_back.png')
(ROOT/'assets/story/aeris-fit-checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
