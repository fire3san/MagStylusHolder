from render_common import *
catalog=json.loads((OUT/'catalog.json').read_text())
for item in catalog:
 t=load_stl(OUT/'stl'/f"{item['id']}.stl")
 t-= (t.reshape(-1,3).min(0)+t.reshape(-1,3).max(0))/2
 im=render([(t,(42,100,101))],w=900,h=720,scale=5.4)
 im.save(OUT/'renders'/f"{item['id']}.png")
canvas=Image.new('RGB',(1800,1440),'white')
for i,it in enumerate(catalog[:4]):
 im=Image.open(OUT/'renders'/f"{it['id']}.png")
 ImageDraw.Draw(im).text((35,35),it['family']+' / '+it['style'],font=ImageFont.truetype(FONT,30),fill='#214649')
 canvas.paste(im,((i%2)*900,(i//2)*720))
canvas.save(OUT/'renders'/'collection.png')
