"""v6: coherent nose loft, vertical BOOX placement, two styles per family.
Dimensions mm. Install manifold3d, trimesh, numpy. Prototype assumptions only.
"""
from geometry import *
import geometry as g
OUT=Path(__file__).resolve().parents[1]
def ring(style):
    # Shallow edge bevel keeps flat underside and preserves hardware cavity.
    s=cyl(34,2.6)+m.Manifold.cylinder(.6,34,33.4,circular_segments=128).translate((0,0,2.6))
    inner=19 if style in ['Flow','Arc'] else 17
    return s-cyl(inner,6,(0,0,-1))
def socket(s,ys):
    for y in ys:s-=cyl(3.15,4.01,(0,y,-.01))
    return s
def cross(style):
    if style=='Flow':
        pts=[(-8,0),(8,0),(8,3.2),(6.2,9.8)]
        pts += [(6.2*math.cos(t),9.8+6.2*math.sin(t)) for t in np.linspace(0,math.pi,65)[1:]]
        pts += [(-8,3.2)]
    else:
        pts=[(-8.5,0),(8.5,0),(8.5,3.2),(7,10),(5.5,14),(2.5,16.1),(-2.5,16.1),(-5.5,14),(-7,10),(-8.5,3.2)]
    return m.CrossSection([pts]).offset(-.35).offset(.35,circular_segments=32)
def section_solid(cs,length,end):return cs.extrude(length).rotate((90,0,0)).translate((0,end,0))
def scabbard(style,apple=False):
    nose=-92.5 if apple else -71.5
    shoulder=nose+8;inner_end=nose+10;z=9.8;bore=9.3 if apple else 9.6
    cs=cross(style);s=section_solid(cs,38-shoulder,38)
    # One shell continues through the taper: no hemispherical tube on a pointed plate.
    stations=[(nose,.04,.08),(nose+.5,.20,.23),(nose+2,.48,.55),(nose+5,.84,.88),(shoulder,1,1)]
    prev=None
    for y,sx,sz in stations:
        p=section_solid(cs.scale((sx,sz)),.04,y)
        if prev is not None:s+=(prev+p).hull()
        prev=p
    s+=ring(style)
    s-=along_y(bore/2,40-inner_end,(40+inner_end)/2,z)
    lead=m.Manifold.cylinder(.9,bore/2+.5,bore/2,circular_segments=96).rotate((90,0,0)).translate((0,38.01,z))
    s-=lead
    ys=[inner_end+8,inner_end+17,inner_end+26]
    # Roof over every socket is integral to shell.
    return socket(s-g.ring_cut(),ys),ys,inner_end+3,z,bore
def km(style,apple=False):
    z=9.3;bore=9.3 if apple else 9.4
    s=ring(style)+rounded(17 if style=='Arc' else 20,62,4.6,5 if style=='Arc' else 3)
    s+=along_y(5.9,54,0,z)
    if style=='Arc':
        # Single centre signature band, merged into the sleeve.
        s+=along_y(6.8,3,0,z)
    else:
        # Two broad low bands, tactile and visually distinct from central collar.
        for y in [-17,17]:s+=along_y(6.6,7,y,z)
    s-=along_y(bore/2,58,0,z)
    s-=box(1.6,58,16,(0,0,z+8))
    return socket(s-g.ring_cut(),[-12,0,12]),[-12,0,12],(-83 if apple else -71.5),z,bore
def tris(s):
    q=s.to_mesh();return np.asarray(q.vert_properties)[:,:3][np.asarray(q.tri_verts)].round(4).tolist()
checks={};catalog=[];scenes={}
def save(name,s):
    assert s.status()==m.Error.NoError and len(s.decompose())==1
    q=s.to_mesh();t=trimesh.Trimesh(np.asarray(q.vert_properties)[:,:3],np.asarray(q.tri_verts),process=True)
    t.export(OUT/'stl'/f'{name}.stl');t=trimesh.load_mesh(OUT/'stl'/f'{name}.stl')
    assert t.is_watertight and t.is_winding_consistent and t.volume>0
    checks[name]={'bounds_mm':t.bounds.round(3).tolist(),'size_mm':t.extents.round(3).tolist(),'volume_cm3':round(t.volume/1000,3),'watertight':True,'winding_consistent':True,'connected_solids':1}
    return t
for family,style,apple in [('S','Flow',False),('S','Facet',False),('KM','Arc',False),('KM','Ribbon',False),('S','Flow',True),('KM','Arc',True)]:
    name=f'{family}_{style}_'+('iPad_Pencil89' if apple else 'BOOX_vertical')
    s,ys,tip,z,bore=scabbard(style,apple) if family=='S' else km(style,apple)
    t=save(name,s);length=166 if apple else 157.5;height=195.4 if apple else 149
    pen=along_y(4.45 if apple else 4.5,length,tip+length/2,z)
    assert (s^pen).volume()<1e-6
    for shift in [10,40,100,180]:assert (s^pen.translate((0,shift,0))).volume()<1e-6
    for y in ys:assert (s^cyl(3,2,(0,y,2))).volume()<1e-6
    lower=min(float(t.bounds[0,1]),tip)
    ring_height=height/2 if apple else 85
    meta={'id':name,'family':family,'style':style,'target':'iPad mini 6/A17 Pro; 8.9mm Pencil fit study' if apple else 'BOOX Go 6 Gen II + InkSense Plus','body_mm':t.extents.round(2).tolist(),'bore_mm':bore,'pen_length_mm':length,'pen_tip_y_mm':tip,'pen_tail_y_mm':tip+length,'assumed_ring_height_from_bottom_mm':ring_height,'bottom_clearance_mm':round(ring_height+lower,2),'top_pen_protrusion_mm':round(max(0,tip+length-(height-ring_height)),2),'minimum_ring_height_for_no_bottom_protrusion_mm':round(-lower,2),'magnet_y_mm':ys,'status':'Digital prototype; actual case position, grip and magnets unverified'}
    catalog.append(meta);scenes[name]=tris(s)
    checks[name]['nominal_pen_collision_mm3']=0
for b,z in [(9.3,9.3),(9.4,9.3),(9.6,9.8)]:
    s=rounded(16,14,4.6,2)+along_y(6.2,12,0,z)-along_y(b/2,16,0,z)
    save(f'fit_bore_{b:.1f}',socket(s,[0]))
save('magnet_spacer_6.05x1.9_qty3_per_holder',cyl(3.025,1.9))
(OUT/'checks.json').write_text(json.dumps(checks,indent=2))
(OUT/'catalog.json').write_text(json.dumps(catalog,indent=2))
(OUT/'scenes.json').write_text(json.dumps(scenes))
print(json.dumps(catalog,indent=2))
