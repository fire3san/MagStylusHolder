"""Compact v2 development prototypes, mm. Python + manifold3d/trimesh/numpy.
Run this file to regenerate STL meshes and checks. No imports from v1 required.
M: optional three pen magnets + clips + strap.
K: keyed TPU collar + clips + strap; no pen magnets required.
The annular case magnet is separate from optional pen magnets.
"""
from pathlib import Path
import math,json
import numpy as np
import manifold3d as m
import trimesh
OUT=Path(__file__).resolve().parents[1]
OUT.joinpath('stl').mkdir(exist_ok=True)
BASE=3.2; ZP=9.3; BORE=9.4; MOUTH=7.8; WALL=1.2
RING_OD=58.4; RING_ID=39.6; RING_DEPTH=2.0
def box(x,y,z,at=(0,0,0)):
    return m.Manifold.cube((x,y,z),True).translate(at)
def cyl(r,h,at=(0,0,0)):
    return m.Manifold.cylinder(h,r,circular_segments=96).translate(at)
def along_y(r,length,y=0,z=ZP):
    return cyl(r,length).rotate((90,0,0)).translate((0,y+length/2,z))
def rounded(w,l,h,r=1,z=0):
    c=m.CrossSection.circle(r,24)
    s=c.translate((-w/2+r,-l/2+r))
    for x,y in [(w/2-r,-l/2+r),(w/2-r,l/2-r),(-w/2+r,l/2-r)]: s+=c.translate((x,y))
    return s.hull().extrude(h).translate((0,0,z))
def clip(bore=BORE):
    ri=bore/2; ro=ri+WALL; a=math.asin(MOUTH/(2*ri))
    ts=np.linspace(math.pi/2+a,math.pi/2-a+2*math.pi,100)
    pts=[(ro*math.cos(t),ro*math.sin(t)) for t in ts]+[(ri*math.cos(t),ri*math.sin(t)) for t in ts[::-1]]
    spring=m.CrossSection([pts]).extrude(7).rotate((90,0,0)).translate((0,3.5,ZP))
    return spring+rounded(13,9,1.1,1,z=2.9)
def base():
    return (cyl(34,BASE)-cyl(17,BASE+2,(0,0,-1)))+rounded(20,65,BASE,2)+rounded(28,14,BASE,2)
def ring_cut():
    return cyl(RING_OD/2,RING_DEPTH+.01,(0,0,-.01))-cyl(RING_ID/2,RING_DEPTH+2,(0,0,-1))
def strap_cut(s):
    for x in [-11,11]: s-=rounded(2.2,10,12,0.7,z=-1).translate((x,0,0))
    return s-box(24,10,.81,(0,0,.395))
def holder(kind):
    s=base()
    for y in [-23,23]: s+=clip().translate((0,y,0))
    if kind=='M':
        # Magnet top at 4.4 mm before thin protective film; barrel bottom at 4.8.
        # Axial magnet pockets accessible from above; they do not open to underside.
        for y in [-12,0,12]:
            boss=cyl(4.7,4.6)
            s+=boss.translate((0,y,0))
            s-=cyl(3.15,5,(0,y,2.4))
    else:
        # Open semicircular saddle with a central flange groove, all inside puck.
        s+=rounded(18,15,ZP,2)
        s-=along_y(5.95,16)
        s-=along_y(7.25,3.6)
        # Clear above centreline for straight top-loading of collar.
        s-=box(15,16,20,(0,0,ZP+10))
    return strap_cut(s-ring_cut())
def collar(bore):
    # Split soft collar. The 3-mm centre flange keys into the 3.6-mm dock groove.
    s=along_y(5.7,12)+along_y(7.0,3)
    s-=along_y(bore/2,14)
    s-=box(1.6,14,15,(0,0,ZP+7.5))
    # Export collar with axis vertical for FDM TPU trial printing.
    return s.translate((0,0,-ZP)).rotate((-90,0,0)).translate((0,0,6))
def collar_in_assembly(bore):
    return collar(bore).translate((0,0,-6)).rotate((90,0,0)).translate((0,0,ZP))

checks={}
def save(name,s,material):
    assert s.status()==m.Error.NoError,(name,s.status())
    mesh=s.to_mesh();t=trimesh.Trimesh(np.asarray(mesh.vert_properties)[:,:3],np.asarray(mesh.tri_verts),process=True)
    t.export(OUT/'stl'/f'{name}.stl');t=trimesh.load_mesh(OUT/'stl'/f'{name}.stl')
    parent=list(range(len(t.vertices)))
    def root(a):
        while parent[a]!=a: parent[a]=parent[parent[a]];a=parent[a]
        return a
    for a,b,c in t.faces: parent[root(int(a))]=root(int(b));parent[root(int(c))]=root(int(b))
    parts=len({root(i) for i in parent})
    assert parts==1 and t.is_watertight and t.is_winding_consistent and t.volume>0
    checks[name]={'material':material,'size_mm':t.extents.round(3).tolist(),'volume_cm3':round(t.volume/1000,3),'watertight':bool(t.is_watertight),'consistent_winding':bool(t.is_winding_consistent),'connected_solids':parts}

def build():
    for kind in ['M','K']: save(f'{kind}_compact_puck_PA12',holder(kind),'PA12 SLS/MJF')
    for bore in [8.6,8.8,9.0]: save(f'K_collar_ID{bore:.1f}_TPU',collar(bore),'TPU 90A-95A trial; do not print rigid')
    for bore in [9.2,9.4,9.6]: save(f'clip_fit_ID{bore:.1f}_PA12',rounded(18,13,BASE,2)+clip(bore),'PA12 SLS/MJF')
    # Three accessible pockets for a simple attraction/polarity bench test.
    test=rounded(14,38,4.6,2)
    for y in [-12,0,12]: test-=cyl(3.15,5,(0,y,2.4))
    save('magnet_test_6x2_PA12',test,'PA12 SLS/MJF')
    save('case_ring_fit_58.4_39.6_2.0_PA12',cyl(34,BASE)-cyl(17,BASE+2,(0,0,-1))-ring_cut(),'PA12 SLS/MJF')
    pen=along_y(4.5,157.5)
    assembly={}
    for kind in ['M','K']:
        h=holder(kind)
        assert (h^pen).volume()<1e-6
        assembly[kind]={'nominal_pen_intersection_mm3':(h^pen).volume(),'pen_axis_z_mm':ZP,'pen_top_z_mm':ZP+4.5,'clip_centres_y_mm':[-23,23]}
    k=holder('K');c=collar_in_assembly(8.8)
    assert (k^c).volume()<1e-6
    # Rigid collision at displacement demonstrates locating shoulders, not strength.
    assert (k^c.translate((0,1,0))).volume()>0
    assembly['K'].update({'collar_dock_collision_mm3':(k^c).volume(),'collar_shift_1mm_collision_mm3':(k^c.translate((0,1,0))).volume(),'axial_flange_clearance_total_mm':.6,'intentional_TPU_bore_interference_diametral_mm':.2,'collar_top_z_mm':16.3,'minimum_web_below_key_and_strap_recess_mm':1.25})
    assembly['M']['magnet_top_z_mm']=4.4
    assembly['M']['nominal_magnet_to_barrel_gap_before_film_mm']=.4
    (OUT/'mesh_checks.json').write_text(json.dumps(checks,indent=2))
    (OUT/'assembly_checks.json').write_text(json.dumps(assembly,indent=2))
    def triangles(s):
        q=s.to_mesh()
        return np.asarray(q.vert_properties)[:,:3][np.asarray(q.tri_verts)].round(5).tolist()
    def section(s,color):
        return {'polygons':[p.tolist() for p in s.rotate((-90,0,0)).slice(0).to_polygons()],'color':color}
    scene={'magnets':[{'triangles':triangles(cyl(3,2,(0,y,8.4)))} for y in [-12,0,12]],'collar':{'triangles':triangles(c.translate((0,0,10)))},'sections':{'M':[section(holder('M'),'#277b82'),section(pen,'#4b5053'),section(cyl(3,2,(0,0,2.4)),'#666b70')],'K':[section(k,'#277b82'),section(pen,'#4b5053'),section(c,'#d08a39')]}}
    (OUT/'preview-scenes.json').write_text(json.dumps(scene))
    print(json.dumps(checks,indent=2));print(json.dumps(assembly,indent=2))
if __name__=='__main__': build()
