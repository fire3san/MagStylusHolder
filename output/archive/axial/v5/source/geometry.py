"""Shared geometry primitives for v5 — inherited from v4 geometry.py with no strap slots."""
from pathlib import Path
import math,json
import numpy as np
import manifold3d as m
import trimesh
OUT=Path(__file__).resolve().parents[1]
OUT.joinpath('stl').mkdir(exist_ok=True)
BASE=3.2; ZP=9.3; BORE=9.4; MOUTH=7.8; WALL=1.2
RING_OD=58.4; RING_ID=39.6; RING_DEPTH=2.0
def box(x,y,z,at=(0,0,0)):
    return m.Manifold.cube((x,y,z),True).translate(at)
def cyl(r,h,at=(0,0,0)):
    return m.Manifold.cylinder(h,r,circular_segments=96).translate(at)
def along_y(r,length,y=0,z=ZP):
    return cyl(r,length).rotate((90,0,0)).translate((0,y+length/2,z))
def rounded(w,l,h,r=1,z=0):
    c=m.CrossSection.circle(r,24)
    s=c.translate((-w/2+r,-l/2+r))
    for x,y in [(w/2-r,-l/2+r),(w/2-r,l/2-r),(-w/2+r,l/2-r)]: s+=c.translate((x,y))
    return s.hull().extrude(h).translate((0,0,z))
def clip(bore=BORE):
    ri=bore/2; ro=ri+WALL; a=math.asin(MOUTH/(2*ri))
    ts=np.linspace(math.pi/2+a,math.pi/2-a+2*math.pi,100)
    pts=[(ro*math.cos(t),ro*math.sin(t)) for t in ts]+[(ri*math.cos(t),ri*math.sin(t)) for t in ts[::-1]]
    spring=m.CrossSection([pts]).extrude(7).rotate((90,0,0)).translate((0,3.5,ZP))
    return spring+rounded(13,9,1.1,1,z=2.9)
def base():
    return (cyl(34,BASE)-cyl(17,BASE+2,(0,0,-1)))+rounded(20,65,BASE,2)+rounded(28,14,BASE,2)
def ring_cut():
    return cyl(RING_OD/2,RING_DEPTH+.01,(0,0,-.01))-cyl(RING_ID/2,RING_DEPTH+2,(0,0,-1))
