from pathlib import Path
import json, math
import numpy as np
import trimesh
from build_models import holder,cyl,BASE,BORE,WALL
out=Path(__file__).resolve().parents[1]
pen=cyl(4.5,157.5).rotate((90,0,0)).translate((0,78.75,BASE+BORE/2+WALL-.3))
checks={}
for guarded,label in [(False,'A_compact'),(True,'B_guarded')]:
    body=holder(guarded,'ring')
    overlap=(body^pen).volume()
    assert overlap < 1e-6
    # Bounding projection at proposed angle, including nominal pen.
    mesh=(body+pen).to_mesh()
    v=np.asarray(mesh.vert_properties)[:,:3]
    t=math.radians(34)
    xy=v[:,:2]@np.array([[math.cos(t),math.sin(t)],[-math.sin(t),math.cos(t)]]).T
    checks[label]={'nominal_cylinder_collision_mm3':overlap,'angle_from_vertical_degrees':34,'centred_assembly_xy_extent_mm':np.ptp(xy,axis=0).round(2).tolist(),'note':'Nominal cylindrical pen only; button, nib profile, case, ring position, flex and magnetic forces unverified.'}
(out/'assembly_checks.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
