import sys,json
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parent))
from geometry import *
p=Path(__file__).resolve().parents[1]
def tri(s):
 q=s.to_mesh();return np.asarray(q.vert_properties)[:,:3][np.asarray(q.tri_verts)].tolist()
scenes={}
for name,tip,z in [('S_Flow_BOOX_vertical',-68.96,9.8),('S_Facet_BOOX_vertical',-58.5,9.8),('KM_Ribbon_BOOX_vertical',-71.5,9.3)]:
 mesh=trimesh.load_mesh(p/'stl'/f'{name}.stl');model=mesh.triangles
 case=rounded(112,152,1.2,9,z=-1.2).translate((0,-10.5,0))
 device=rounded(109,149,6.8,8,z=-8).translate((0,-10.5,0))
 pen=along_y(4.5,157.5,tip+157.5/2,z)
 scenes[name]=[[tri(device),[58,64,61]],[tri(case),[191,186,170]],[model.tolist(),[55,107,101]],[tri(pen),[223,220,204]]]
(p/'context-scenes.json').write_text(json.dumps(scenes))
