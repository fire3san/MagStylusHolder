"""Provisional v0.1 prototypes. Millimetres. pip install manifold3d trimesh numpy.
Run from any directory. Regenerates ../stl and ../mesh_checks.json.
Hardware dimensions are assumptions, not a MagSafe standard.
"""
from pathlib import Path
import math, json
import numpy as np
import manifold3d as m
import trimesh

OUT = Path(__file__).resolve().parents[1]
BASE = 3.2
BORE = 9.4
WALL = 1.2
MOUTH = 7.8
RING_OD, RING_ID, RING_DEPTH = 58.4, 47.6, 2.0
MAGNET_PCD, MAGNET_D, MAGNET_DEPTH = 54, 5.3, 2.15

def box(x,y,z,at=(0,0,0)):
    return m.Manifold.cube((x,y,z),True).translate(at)

def cyl(r,h,at=(0,0,0)):
    return m.Manifold.cylinder(h,r,circular_segments=96).translate(at)

def rounded(w,l,h,r=2,z=0):
    c=m.CrossSection.circle(r,32)
    s=c.translate((-w/2+r,-l/2+r))
    for x,y in [(w/2-r,-l/2+r),(w/2-r,l/2-r),(-w/2+r,l/2-r)]:
        s=s+c.translate((x,y))
    return s.hull().extrude(h).translate((0,0,z))

def clip(bore=BORE, mouth=MOUTH, length=8):
    ri=bore/2; ro=ri+WALL; zc=BASE+ro-0.3
    # Continuous circular spring section; 7.8 mm mouth at inner lip.
    a=math.asin(mouth/(2*ri))
    ang=np.linspace(math.pi/2+a,math.pi/2-a+2*math.pi,100)
    pts=[(ro*math.cos(t),ro*math.sin(t)) for t in ang]
    pts += [(ri*math.cos(t),ri*math.sin(t)) for t in ang[::-1]]
    spring=m.CrossSection([pts]).extrude(length).rotate((90,0,0)).translate((0,length/2,zc))
    foot=rounded(13, length+2,0.9,1,z=BASE-0.4)
    return spring+foot

def mount(style):
    # Open annulus saves material; spine crosses centre.
    s=cyl(32,BASE)-cyl(21,BASE+2,(0,0,-1))
    if style=='ring':
        recess=cyl(RING_OD/2,RING_DEPTH+0.01,(0,0,-0.01))-cyl(RING_ID/2,RING_DEPTH+2,(0,0,-1))
        s=s-recess
    else:
        for i in range(12):
            t=2*math.pi*i/12
            s=s-cyl(MAGNET_D/2,MAGNET_DEPTH+0.01,(MAGNET_PCD/2*math.cos(t),MAGNET_PCD/2*math.sin(t),-0.01))
    return s

def holder(protected,style):
    length=166.5 if protected else 94
    s=mount(style)+rounded(14.4,length,BASE,2.5)
    for y in [-40,40]:
        s=s+rounded(24,14,BASE,2).translate((0,y,0))
        s=s+clip().translate((0,y,0))
    if protected:
        # Low side rails and open-top end guards. Nib has no custom shoulder seat.
        shell=rounded(14.4,length,11.0,2.5,z=BASE-0.2)
        cavity=rounded(11.4,length-3,12,1,z=BASE+0.8)
        shell=shell-cavity
        # Lower central side rails to 5.2 mm; retain 16 mm guards at each end.
        shell=shell-box(30,length-32,20,(0,0,BASE+12))
        s=s+shell
    for y in [-40,40]:
        for x in [-9.3,9.3]:
            s=s-rounded(2.0,10.0,BASE+2,0.6,z=-1).translate((x,y,0))
        # Band recess underneath: 0.8 mm deep, does not add to installed thickness.
        s=s-box(21,10,0.81,(0,y,0.395))
    # Reapply hardware cavities after spine union, so pockets are not obstructed.
    full=cyl(32,BASE)
    cavities=full-mount(style)
    # Only recesses: exclude the central lightweight cutout from this subtraction.
    cavities=cavities-cyl(21,BASE+2,(0,0,-1))
    s=s-cavities
    return s

checks={}
def save(name,s):
    assert s.status()==m.Error.NoError, (name,s.status())
    mesh=s.to_mesh()
    t=trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:,:3],faces=np.asarray(mesh.tri_verts),process=True)
    t.export(OUT/'stl'/f'{name}.stl')
    # Reopen the exact exported STL for validation.
    t=trimesh.load_mesh(OUT/'stl'/f'{name}.stl')
    assert t.is_watertight and t.is_winding_consistent and t.volume>0
    parent=list(range(len(t.vertices)))
    def root(a):
        while parent[a]!=a:
            parent[a]=parent[parent[a]]; a=parent[a]
        return a
    for a,b,c in t.faces:
        parent[root(int(a))]=root(int(b)); parent[root(int(c))]=root(int(b))
    components=len({root(i) for i in range(len(parent))})
    assert components==1, (name,components)
    checks[name]={'watertight':bool(t.is_watertight),'consistent_winding':bool(t.is_winding_consistent),'connected_solids':components,'bounds_mm':t.bounds.round(3).tolist(),'size_mm':t.extents.round(3).tolist(),'volume_cm3':round(t.volume/1000,3),'nylon_mass_estimate_g_at_1_01':round(t.volume/1000*1.01,2),'triangles':len(t.faces)}

for protected,label in [(False,'A_compact'),(True,'B_guarded')]:
    for style in ['ring','discs']:
        save(f'{label}_{style}_PROVISIONAL',holder(protected,style))
for d in [9.2,9.4,9.6]:
    save(f'fit_clip_ID_{d:.1f}',rounded(18,16,BASE,2)+clip(d))
save('fit_disc_pocket_5.3x2.15',rounded(12,12,BASE,2)-cyl(MAGNET_D/2,MAGNET_DEPTH+0.01,(0,0,-0.01)))
save('fit_ring_recess_58.4_47.6_2.0',mount('ring'))
(OUT/'mesh_checks.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
