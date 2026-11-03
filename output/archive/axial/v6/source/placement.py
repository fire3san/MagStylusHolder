from render_common import *
im=Image.new('RGB',(1200,820),'#f4f3ef');d=ImageDraw.Draw(im);font=ImageFont.truetype(FONT,24);small=ImageFont.truetype(FONT,18)
for i,(title,tip,tail,body) in enumerate([('S / Flow + Facet',-58.5,99,-71.54),('K+M / Arc + Ribbon',-71.5,86,-34)]):
 x=100+i*590;y=220;k=3;cx=x+163.5;cy=y+64*k
 d.text((x,25),title,font=font,fill='#214649')
 d.rounded_rectangle((x,y,x+327,y+447),18,outline='#73847e',width=3)
 d.ellipse((cx-102,cy-102,cx+102,cy+102),outline='#427c7a',width=18)
 d.rounded_rectangle((cx-24,cy-38*k,cx+24,cy-body*k),10,fill='#588987')
 d.rounded_rectangle((cx-10,cy-tail*k,cx+10,cy-tip*k),7,fill='#323c37')
 d.line((x-10,y+447,x+340,y+447),fill='#c19b35',width=4)
 d.text((x,y+465),f'Bottom clearance: {85+min(tip,body):.2f} mm',font=small,fill='#53604c')
 d.text((x,90),f'Tail above top: {max(0,tail-64):.1f} mm',font=small,fill='#53604c')
 d.text((x,730),'Ring centre: 85 mm above device bottom',font=small,fill='#323c37')
d.text((100,780),'Nominal placement only. K+M has no axial stop; sliding changes clearance.',font=small,fill='#8a542d')
im.save(OUT/'renders'/'vertical_placement.png')
