import sys,json
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parent))
from render_common import *
p=Path(__file__).resolve().parents[1]
for name,scene in json.loads((p/'context-scenes.json').read_text()).items():
 objs=[]
 for ts,c in scene:
  t=np.array(ts);t[:,:,1]+=4
  objs.append((t,c))
 render(objs,w=1000,h=1000,scale=4.6,rx=-25,rz=-22).save(p/'renders'/f'{name}_mounted.png')

canvas=Image.new('RGB',(1600,980),'#f4f3ef')
for i,(name,label) in enumerate([('S_Flow_BOOX_vertical','FLOW LONG / 120.00 mm'),('S_Facet_BOOX_vertical','FACET SHORT / 109.54 mm')]):
 im=Image.open(p/'renders'/f'{name}_mounted.png').resize((800,800))
 canvas.paste(im,(i*800,80))
 d=ImageDraw.Draw(canvas);f=ImageFont.truetype(FONT,28);small=ImageFont.truetype(FONT,22)
 d.text((i*800+50,30),label,font=f,fill='#214649')
 d.text((i*800+50,885),'Bottom: '+('3.00 mm / Tail: 24.54 mm' if i==0 else '13.46 mm / Tail: 35.00 mm'),font=small,fill='#214649')
ImageDraw.Draw(canvas).text((50,940),'85 mm ring height. Actual holder CAD; device and pen are dimensional illustrations.',font=ImageFont.truetype(FONT,21),fill='#65735e')
canvas.save(p/'renders'/'flow_facet_comparison.png')
