from geometry import *
import geometry as g
OUT=Path(__file__).resolve().parents[1]
def softbox(w,l,h,r,at):
    s=None
    for x in [-w/2+r,w/2-r]:
        for y in [-l/2+r,l/2-r]:
            for z in [r,h-r]:
                p=m.Manifold.sphere(r,24).translate((x,y,z))
                s=p if s is None else s+p
    return s.hull().translate(at)
def sockets(s,ys):
    for y in ys:s-=cyl(3.15,4.01,(0,y,-.01))
    return s
def softcapsule(w,l,h,r,at):
    parts=[]
    for y in [-l/2+w/2,l/2-w/2]:
        for z in [r,h-r]:
            for a in np.linspace(0,2*math.pi,24,endpoint=False):
                parts.append(m.Manifold.sphere(r,16).translate(((w/2-r)*math.cos(a),y+(w/2-r)*math.sin(a),z)))
    s=parts[0]
    for p in parts[1:]:s+=p
    return s.hull().translate(at)
def km():
    s=(cyl(34,3.2)-cyl(17,5,(0,0,-1)))+rounded(20,65,3.2,3)
    # Original orange collar silhouette: sleeve plus centre flange, fused to base.
    s+=along_y(5.7,12)+along_y(7,3)
    s+=rounded(14,36,4.6,3)
    s-=along_y(4.7,38)
    s-=box(1.6,14,15,(0,0,16.8))
    for y in [-23,23]:s+=g.clip().translate((0,y,0))
    return sockets(s-g.ring_cut(),[-12,0,12])
def sheath():
    # One continuous tube with hemispherical external nose and rounded base rail.
    s=(cyl(34,3.2)-cyl(17,5,(0,0,-1)))+softcapsule(16,128,3.2,1.2,(0,-21,0))
    tube=along_y(6.2,116,-20,9.8)+m.Manifold.sphere(6.2,96).translate((0,-78,9.8))
    # Smooth bridge into the rail, with softened longitudinal edge transitions.
    foot=softbox(14,118,4.4,1.2,(0,-20,0))
    s+=tube+foot
    # Bore opens at +38, terminates at -80: ~1.25 mm nib clearance at centred pen.
    s-=along_y(4.8,119,-20.5,9.8)
    # Conical entry lead-in, 0.8 mm long; no second guide ring.
    lead=m.Manifold.cylinder(.8,5.3,4.8,circular_segments=96).rotate((90,0,0)).translate((0,38.01,9.8))
    s-=lead
    return sockets(s-g.ring_cut(),[-68,-54,-40])
def tris(s):
    q=s.to_mesh();return np.asarray(q.vert_properties)[:,:3][np.asarray(q.tri_verts)].round(5).tolist()
results={};scenes={}
def save(name,s):
    assert s.status()==m.Error.NoError and len(s.decompose())==1
    q=s.to_mesh();t=trimesh.Trimesh(np.asarray(q.vert_properties)[:,:3],np.asarray(q.tri_verts),process=True)
    t.export(OUT/'stl'/f'{name}.stl');t=trimesh.load_mesh(OUT/'stl'/f'{name}.stl')
    assert t.is_watertight and t.is_winding_consistent and t.volume>0
    results[name]={'size_mm':t.extents.round(3).tolist(),'volume_cm3':round(t.volume/1000,3),'watertight':True,'winding_consistent':True,'connected_solids':1}
for name,s,z in [('KM_fused_collar_under_magnets',km(),9.3),('S_single_tunnel_rounded',sheath(),9.8)]:
    save(name,s)
    pen=along_y(4.5,157.5,0,z)
    assert (s^pen).volume()<1e-6
    for dy in [10,30,60,100,160]:assert (s^pen.translate((0,dy,0))).volume()<1e-6
    ys=[-12,0,12] if name.startswith('KM') else [-68,-54,-40]
    for y in ys:assert (s^cyl(3,2,(0,y,2))).volume()<1e-6
    results[name]['nominal_pen_collision_mm3']=0
    scenes[name]=tris(s)
save('magnet_spacer_6.05x1.9_print_3_per_holder',cyl(3.025,1.9))
# Test pieces preserve respective enclosed bore and underside socket stack.
for bore,z,label in [(9.4,9.3,'KM'),(9.6,9.8,'S')]:
    s=rounded(16,14,4.6,2)+along_y(6.2,12,0,z)-along_y(bore/2,16,0,z)
    s=sockets(s,[0]);save(f'{label}_bore_and_socket_sample',s)
(OUT/'checks.json').write_text(json.dumps(results,indent=2))
(OUT/'scenes.json').write_text(json.dumps(scenes))
print(json.dumps(results,indent=2))
