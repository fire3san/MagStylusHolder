"""Additional v3 prototypes, mm. Run with manifold3d, trimesh and numpy installed."""
import geometry as g
from geometry import m,np,trimesh,Path,json,math,box,cyl,along_y,rounded
OUT=Path(__file__).resolve().parents[1]
def cuff(bore=9.2):
    ri=bore/2;ro=ri+1.2;a=math.asin(7.6/(2*ri))
    ts=np.linspace(math.pi/2+a,math.pi/2-a+2*math.pi,120)
    p=[(ro*math.cos(t),ro*math.sin(t)) for t in ts]+[(ri*math.cos(t),ri*math.sin(t)) for t in ts[::-1]]
    return m.CrossSection([p]).extrude(12).rotate((90,0,0)).translate((0,6,9.3))+rounded(13.6,14,1.1,1,z=2.9)
def compact(magnets):
    s=g.base()
    for y in [-23,23]:s+=cuff().translate((0,y,0))
    if magnets:
        for y in [-12,0,12]:
            s+=cyl(4.7,4.6,(0,y,0))
            s-=cyl(3.15,6,(0,y,2.4))
    return g.strap_cut(s-g.ring_cut())
def scabbard():
    # Rear cap removed; lower blind sheath and separate entry guide retained.
    s=g.base()+rounded(16,126,3.2,2).translate((0,-21,0))
    s+=rounded(15,56,4.2,1).translate((0,-56,0))
    s+=along_y(6.2,56,-56,9.8)
    # Closed end -84; inner stop -82.4; nominal pen tip -78.75 leaves 3.65 mm.
    s-=along_y(4.8,55,-54.9,9.8)
    s+=rounded(15,14,4.2,1).translate((0,32,0))
    s+=along_y(6.2,12,32,9.8)
    s-=along_y(4.8,16,32,9.8)
    # Three underside-loaded magnet sockets, ceiling at z4.4; bore floor z5.0.
    for y in [-68,-54,-40]:s-=cyl(3.15,4.41,(0,y,-.01))
    return g.strap_cut(s-g.ring_cut())
def save(name,s,material='PA12 SLS/MJF'):
    assert s.status()==m.Error.NoError
    q=s.to_mesh();t=trimesh.Trimesh(np.asarray(q.vert_properties)[:,:3],np.asarray(q.tri_verts),process=True)
    t.export(OUT/'stl'/f'{name}.stl');t=trimesh.load_mesh(OUT/'stl'/f'{name}.stl')
    assert t.is_watertight and t.is_winding_consistent and t.volume>0
    assert len(s.decompose())==1
    results[name]={'size_mm':t.extents.round(3).tolist(),'volume_cm3':round(t.volume/1000,3),'watertight':bool(t.is_watertight),'consistent_winding':bool(t.is_winding_consistent),'connected_solids':len(s.decompose()),'material':material}
    return s
def triangles(s):
    q=s.to_mesh();return np.asarray(q.vert_properties)[:,:3][np.asarray(q.tri_verts)].round(5).tolist()
results={};scenes={};checks={}
for name,s,z in [('S_scabbard_3magnets',scabbard(),9.8),('K2_integral_dual_cuffs',compact(False),9.3),('MK2_integral_dual_cuffs_3magnets',compact(True),9.3)]:
    save(name,s);pen=along_y(4.5,157.5,0,z)
    assert (s^pen).volume()<1e-6
    # Check nominal pen's unobstructed axial route from the upper end of S.
    if name.startswith('S_'):
        for shift in [10,30,60,100,160]:assert (s^pen.translate((0,shift,0))).volume()<1e-6
    checks[name]={'nominal_pen_collision_mm3':(s^pen).volume(),'pen_axis_z_mm':z,'note':'9 mm smooth cylindrical envelope only; button/taper, forces, fatigue and magnetic response untested.'}
    scenes[name]={'body':triangles(s),'magnets':[]}
    ys=[-68,-54,-40] if name.startswith('S_') else ([-12,0,12] if name.startswith('MK') else [])
    for y in ys:
        mag=cyl(3,2,(0,y,2.4))
        assert (s^mag).volume()<1e-6
        scenes[name]['magnets'].append(triangles(mag))
for bore in [9.0,9.2,9.4]:save(f'cuff_fit_ID{bore:.1f}',rounded(18,18,3.2,2)+cuff(bore))
tunnel=rounded(15,14,4.2,1)+along_y(6.2,12,0,9.8)-along_y(4.8,16,0,9.8)
save('tunnel_fit_ID9.6',tunnel)
save('S_magnet_spacer_print_3',cyl(3.025,2.3))
# Cutaway coupon includes exact blind socket, roof and tunnel floor.
coupon=rounded(15,14,4.2,1)+along_y(6.2,12,0,9.8)-along_y(4.8,16,0,9.8)-cyl(3.15,4.41,(0,0,-.01))
save('S_socket_tunnel_test',coupon)
checks['S_magnet_stack']={'socket_diameter_mm':6.3,'socket_depth_mm':4.4,'magnet_mm':[6,2],'spacer_mm':[6.05,2.3],'bond_allowance_mm':.1,'roof_below_bore_mm':.6,'nominal_magnet_to_pen_gap_mm':.9,'closure':'Bond spacer and protective film; not a snap fit.'}
(OUT/'mesh_checks.json').write_text(json.dumps(results,indent=2))
(OUT/'assembly_checks.json').write_text(json.dumps(checks,indent=2))
(OUT/'preview_scenes.json').write_text(json.dumps(scenes))
print(json.dumps(results,indent=2))
