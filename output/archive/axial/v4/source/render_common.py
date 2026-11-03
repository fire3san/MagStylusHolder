"""Render exact CAD meshes with a depth buffer; optional hardware is colour coded."""
from pathlib import Path
import json,math,struct
import numpy as np
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parents[1]
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
def load_stl(p):
    b=p.read_bytes(); n=struct.unpack_from('<I',b,80)[0]
    return np.array([struct.unpack_from('<12f',b,84+50*i)[3:] for i in range(n)]).reshape(-1,3,3)
def render(objects,w=640,h=470,scale=5.3,rx=-48,rz=-28):
    out=np.full((h,w,3),(244,243,239),dtype=np.uint8); depth=np.full((h,w),-1e10)
    a=math.radians(rx);b=math.radians(rz)
    mat=np.array([[1,0,0],[0,math.cos(a),-math.sin(a)],[0,math.sin(a),math.cos(a)]])@np.array([[math.cos(b),-math.sin(b),0],[math.sin(b),math.cos(b),0],[0,0,1]])
    light=np.array([.2,-.4,.9]);light/=np.linalg.norm(light)
    for tris,col in objects:
        for tri in tris:
            t=tri@mat.T; norm=np.cross(t[1]-t[0],t[2]-t[0]); ln=np.linalg.norm(norm)
            if ln<1e-9:continue
            c=np.array(col)*(.45+.55*abs(np.dot(norm/ln,light)))
            xy=t[:,:2]*[scale,-scale]+[w/2,h/2+20]
            x0=max(0,int(np.floor(xy[:,0].min())));x1=min(w-1,int(np.ceil(xy[:,0].max())))
            y0=max(0,int(np.floor(xy[:,1].min())));y1=min(h-1,int(np.ceil(xy[:,1].max())))
            if x1<x0 or y1<y0:continue
            xx,yy=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
            (ax,ay),(bx,by),(cx,cy)=xy
            den=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
            if abs(den)<1e-9:continue
            u=((by-cy)*(xx-cx)+(cx-bx)*(yy-cy))/den
            v=((cy-ay)*(xx-cx)+(ax-cx)*(yy-cy))/den;ww=1-u-v
            zz=u*t[0,2]+v*t[1,2]+ww*t[2,2]
            region=depth[y0:y1+1,x0:x1+1];mask=(u>=-1e-6)&(v>=-1e-6)&(ww>=-1e-6)&(zz>region)
            region[mask]=zz[mask];out[y0:y1+1,x0:x1+1][mask]=c.astype(np.uint8)
    return Image.fromarray(out)
