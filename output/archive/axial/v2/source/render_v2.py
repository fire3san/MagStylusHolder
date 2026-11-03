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
def main():
    scene=json.loads((OUT/'preview-scenes.json').read_text())
    im=Image.new('RGB',(1500,1200),(244,243,239));d=ImageDraw.Draw(im)
    def txt(x,y,s,size=24):d.text((x,y),s,font=ImageFont.truetype(FONT,size),fill='#26383d')
    txt(50,28,'Two compact prototypes | same 68 mm puck footprint',36)
    txt(50,83,'Teal = printed PA12   /   orange = soft TPU collar   /   silver = purchased magnets',22)
    for kind,x in [('M',40),('K',780)]:
        tris=load_stl(OUT/'stl'/f'{kind}_compact_puck_PA12.stl')
        objs=[(tris,(65,142,148))]
        if kind=='M':objs += [(np.array(o['triangles']),(184,190,195)) for o in scene['magnets']]
        if kind=='K':objs += [(np.array(scene['collar']['triangles']),(224,142,69))]
        im.paste(render(objs),(x,145))
    txt(60,135,'M / Three pen magnets + clips',27)
    txt(800,135,'K / Keyed collar + clips',27)
    txt(60,615,'Magnets shown lifted above their top-loading pockets.',20)
    txt(800,615,'Collar shown lifted above its locating groove.',20)
    # Diagram sections are generated from CAD cross sections, not inferred artwork.
    for kind,x in [('M',70),('K',810)]:
        txt(x,685,'Centre detail — '+kind+' (strap route schematic)',22)
        ox=x+280;oy=955;s=14
        for item in scene['sections'][kind]:
            for poly in item['polygons']:
                for p,q in zip(poly,poly[1:]+poly[:1]):
                    p=np.array(p);q=np.array(q);delta=q-p;lo=0.;hi=1.
                    if abs(delta[0])<1e-9:
                        if abs(p[0])>16:continue
                    else:
                        ts=sorted([(-16-p[0])/delta[0],(16-p[0])/delta[0]])
                        lo=max(lo,ts[0]);hi=min(hi,ts[1])
                        if lo>hi:continue
                    pts=[p+lo*delta,p+hi*delta]
                    d.line([(ox+a*s,oy-b*s) for a,b in pts],fill=item['color'],width=3)
        # 8 mm purchased strap follows the top of the pen/collar and both slots.
        ztop=14.25 if kind=='M' else 16.9
        points=[(-11,.4),(-11,ztop-3),(-5,ztop),(5,ztop),(11,ztop-3),(11,.4),(-11,.4)]
        d.line([(ox+a*s,oy-b*s) for a,b in points],fill='#8562b5',width=5)
        txt(x,990,'Purple line = soft strap through both slots',20)
    txt(60,1060,'M: attraction is unverified. Strap is needed for travel.',22)
    txt(800,1060,'K: strap holds collar down; TPU grip must be tested.',22)
    txt(60,1120,'Pen ends remain exposed. These are fit-test prototypes, not drop-protection products.',23)
    im.save(OUT/'compact-v2-explained.png')
if __name__=='__main__':main()
