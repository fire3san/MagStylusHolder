"""Two original side-mounted concepts, mm. Run with project .venv Python.
Side concepts plus an edited reference STL. Hardware dimensions are provisional.
"""
from geometry import *
from render_common import render, Image, ImageDraw, ImageFont, FONT
import zipfile
OUT=Path(__file__).resolve().parents[1]
RING_OD=58.4; RING_ID=39.6; RING_DEPTH=2.0
MAGNET_D=5.0; MAGNET_T=1.0; POCKET_D=5.3; POCKET_DEPTH=3.0
TAPE_T=0.2; SPACER_T=1.8 # provisional adhesive allowance
# 85 mm interpreted from pen's right tangent to ring's far right hardware edge.
PEN_D=9.0; BORE=9.6; X=-(85+PEN_D/2-RING_OD/2)
Z=8.6; WALL=1.5; BASE_T=3.4
def ring():
    return cyl(32.5,BASE_T)-cyl(17.5,BASE_T+2,(0,0,-1))
def pockets(s,ys):
    # Cut after all unions so the bridge cannot obstruct the hardware recess.
    ring_recess=cyl(RING_OD/2,RING_DEPTH+.01,(0,0,-.01))-cyl(RING_ID/2,RING_DEPTH+2,(0,0,-1))
    s-=ring_recess
    for y in ys:
        s-=cyl(POCKET_D/2,POCKET_DEPTH+.01,(X,y,-.01))
        assert (s^cyl(MAGNET_D/2,MAGNET_T,(X,y,SPACER_T))).volume()<1e-6
    return s
def arm():
    # Wide tapered bridge; reaches solid material inside ring recess.
    return m.CrossSection([[(X-6,-10),(-21,-14),(-21,14),(X-6,10)]]).extrude(BASE_T)
def scabbard():
    # Flow-style continuous rounded cross-section and a soft sword-shaped nose.
    pts=[(-7,0),(7,0),(7,3.4),(6.3,8.6)]
    pts += [(6.3*math.cos(t),8.6+6.3*math.sin(t)) for t in np.linspace(0,math.pi,65)[1:]]
    pts += [(-7,3.4)]
    cs=m.CrossSection([pts]).offset(-.35).offset(.35,circular_segments=32)
    def station(y,sx,sz):
        return cs.scale((sx,sz)).extrude(.04).rotate((90,0,0)).translate((X,y,0))
    shell=cs.extrude(76.2).rotate((90,0,0)).translate((X,12,0))
    prev=None
    for y,sx,sz in [(-82,.08,.12),(-80,.24,.32),(-76,.53,.63),(-70,.84,.9),(-64,1,1)]:
        part=station(y,sx,sz)
        if prev is not None:shell+=(prev+part).hull()
        prev=part
    shell-=along_y(BORE/2,80,-26,Z).translate((X,0,0))
    shell-=box(16,12,12,(X,12,Z+6))
    shell-=box(3,40,12,(X,-14,Z+7))
    return ring()+arm()+shell
def quickclip():
    s=ring()+arm()+rounded(14,42,4.2,3).translate((X,0,0))
    ri=BORE/2;ro=ri+WALL;mouth=7.6;a=math.asin(mouth/(2*ri))
    ts=np.linspace(math.pi/2+a,math.pi/2-a+2*math.pi,100)
    pts=[(ro*math.cos(t),ro*math.sin(t)) for t in ts]+[(ri*math.cos(t),ri*math.sin(t)) for t in ts[::-1]]
    for y in [-13,13]:
        s+=m.CrossSection([pts]).extrude(10).rotate((90,0,0)).translate((X,y+5,Z))
    # Relief between the clips keeps button clear and reduces material.
    s-=along_y(ri,44,0,Z).translate((X,0,0))
    return s
checks={};items=[]
for name,solid,ys in [('01_Side_Scabbard_PROVISIONAL',pockets(scabbard(),[-60,-48,-36,-24,-12]),[-60,-48,-36,-24,-12]),('02_Side_QuickClip_PROVISIONAL',pockets(quickclip(),[-13,0,13]),[-13,0,13])]:
    assert solid.status()==m.Error.NoError and len(solid.decompose())==1
    solid=solid.simplify(.001)
    q=solid.to_mesh();t=trimesh.Trimesh(np.asarray(q.vert_properties)[:,:3],np.asarray(q.tri_verts),process=True)
    p=OUT/'stl'/f'{name}.stl';t.export(p);t=trimesh.load_mesh(p)
    assert t.is_watertight and t.is_winding_consistent and t.volume>0
    checks[name]={'watertight':bool(t.is_watertight),'connected_solids':len(solid.decompose()),'size_mm':t.extents.round(2).tolist(),'volume_cm3':round(t.volume/1000,2)}
    checks[name].update(magnet_count=len(ys),magnet_centres_xy_mm=[[X,y] for y in ys],magnet_mm=[MAGNET_D,MAGNET_T],pocket_mm=[POCKET_D,POCKET_DEPTH],spacer_thickness_mm=SPACER_T,assumed_tape_mm=TAPE_T,nominal_magnet_collision_mm3=0)
    v=t.triangles.copy();v-=(t.bounds[0]+t.bounds[1])/2
    im=render([(v,(42,100,101))],w=900,h=760,scale=6,rx=-48,rz=-20)
    im.save(OUT/f'{name}.png');items.append(im)
    render([(v,(42,100,101))],w=900,h=760,scale=6,rx=145,rz=-20).save(OUT/f'{name}_underside.png')
canvas=Image.new('RGB',(1800,900),(244,243,239));d=ImageDraw.Draw(canvas)
for i,im in enumerate(items):
    canvas.paste(im,(900*i,100))
    d.text((50+900*i,38),['01 / SIDE SCABBARD','02 / SIDE QUICK CLIP'][i],font=ImageFont.truetype(FONT,28),fill='#20494a')
    d.text((50+900*i,850),'DIMENSIONAL CONCEPT / MAGNET FIT TO BE CONFIRMED',font=ImageFont.truetype(FONT,18),fill='#555555')
canvas.save(OUT/'two_designs.png')
q=cyl(2.525,SPACER_T).to_mesh()
trimesh.Trimesh(np.asarray(q.vert_properties)[:,:3],np.asarray(q.tri_verts)).export(OUT/'stl'/'spacer_5.05x1.80.stl')
(OUT/'checks.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))

# Third design edits the exact user-supplied STL, retaining its clips and outline.
reference=Path(__file__).resolve().parents[3]/'Apple_Pencil_magnetic_clip.stl'
t=trimesh.load_mesh(reference)
original=m.Manifold(m.Mesh(np.asarray(t.vertices,dtype=np.float32),np.asarray(t.faces,dtype=np.uint32)))
assert original.status()==m.Error.NoError
third=original+box(12.0,23.0,.7,(0,16.75,2.05)) # fills engraved lettering to z=2.4
for y in [0,16.75,33.5]:
    third+=cyl(5.4,2.4,(0,y,0)) # fill old magnet recess without changing the clips
    third-=cyl(2.65,1.21,(0,y,-.01)) # 1mm magnet + provisional .2mm adhesive
    assert (third^cyl(2.5,1,(0,y,0))).volume()<1e-6
assert third.status()==m.Error.NoError and len(third.decompose())==1
q=third.to_mesh();t=trimesh.Trimesh(np.asarray(q.vert_properties)[:,:3],np.asarray(q.tri_verts),process=True)
name='03_Apple_Pencil_Original_5x1_NoText_PROVISIONAL'
p=OUT/'stl'/f'{name}.stl';t.export(p);t=trimesh.load_mesh(p)
assert t.is_watertight and t.is_winding_consistent and t.volume>0
checks[name]={'watertight':True,'connected_solids':1,'size_mm':t.extents.round(3).tolist(),'magnet_count':3,'magnet_mm':[5,1],'pocket_mm':[5.3,1.2],'pocket_centres_xy_mm':[[0,0],[0,16.75],[0,33.5]],'original_clip_geometry_retained':True,'engraving_filled_to_z_mm':2.4}
v=t.triangles.copy();v-=(t.bounds[0]+t.bounds[1])/2
for label,rx in [('top',-48),('underside',145)]:
    render([(v,(42,100,101))],w=900,h=760,scale=8,rx=rx,rz=-20).save(OUT/f'{name}_{label}.png')
checks['clearance']={'pen_axis_to_ring_centre_mm':abs(X),'holder_edge_to_ring_edge_min_horizontal_mm':abs(X)-7-32.5,'pen_tangent_to_ring_hardware_far_edge_mm':abs(X)-PEN_D/2+RING_OD/2,'quickclip_centres_apart_mm':26,'quickclip_clear_gap_mm':16,'case_fit_verified':False}
(OUT/'checks.json').write_text(json.dumps(checks,indent=2))
