"""Render the exported STL triangles with Pillow, no CAD viewer required."""
from pathlib import Path
import struct, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
OUT=Path(__file__).resolve().parents[1]
im=Image.new('RGB',(1600,1100),'#f2f1ec'); draw=ImageDraw.Draw(im)
font='/System/Library/Fonts/Supplemental/Arial.ttf'
def text(x,y,s,size=24):
    draw.text((x,y),s,fill='#233235',font=ImageFont.truetype(font,size))
def render(name,origin,scale=4,underside=False):
    data=(OUT/'stl'/name).read_bytes(); n=struct.unpack_from('<I',data,80)[0]
    faces=[]
    ax=math.radians(52 if not underside else 132); az=math.radians(-28)
    rz=np.array([[math.cos(az),-math.sin(az),0],[math.sin(az),math.cos(az),0],[0,0,1]])
    rx=np.array([[1,0,0],[0,math.cos(ax),-math.sin(ax)],[0,math.sin(ax),math.cos(ax)]])
    mat=rx@rz
    for i in range(n):
        v=np.array(struct.unpack_from('<12f',data,84+50*i)[3:]).reshape(3,3)@mat.T
        normal=np.cross(v[1]-v[0],v[2]-v[0]); norm=np.linalg.norm(normal)
        if norm==0: continue
        normal/=norm
        shade=.55+.45*abs(np.dot(normal,np.array([.25,-.45,.86])))
        color=tuple(int(c*shade) for c in (72,135,139))
        pts=[(origin[0]+p[0]*scale,origin[1]-p[1]*scale) for p in v]
        faces.append((v[:,2].mean(),pts,color))
    for _,pts,c in sorted(faces,key=lambda a:a[0]): draw.polygon(pts,fill=c)
text(65,35,'BOOX stylus holder | v0.1 prototype geometry',38)
text(65,89,'Actual exported STL meshes. Hardware, straps and pen omitted.',23)
text(80,155,'A / Compact clips',29); text(850,155,'B / Guarded cradle',29)
render('A_compact_ring_PROVISIONAL.stl',(380,420),5)
render('B_guarded_ring_PROVISIONAL.stl',(1160,400),3.7)
text(80,650,'Ring insert underside',26);text(850,650,'12-disc underside',26)
render('A_compact_ring_PROVISIONAL.stl',(370,850),4,True)
render('A_compact_discs_PROVISIONAL.stl',(1140,850),4,True)
text(65,1040,'Provisional hardware fit. Print fit coupons first. Dimensions in millimetres.',23)
im.save(OUT/'model-preview.png')
