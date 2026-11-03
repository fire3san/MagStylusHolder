from render_common import *
scene=json.loads((OUT/'preview_scenes.json').read_text())
im=Image.new('RGB',(1650,790),(244,243,239));d=ImageDraw.Draw(im)
def text(x,y,s,size=24):d.text((x,y),s,font=ImageFont.truetype(FONT,size),fill='#26383d')
text(40,25,'Three additional prototypes | v3',36)
text(40,80,'Actual CAD geometry. Silver discs are purchased magnets, shown lifted out for clarity.',23)
items=[('S_scabbard_3magnets','S / Scabbard',3.4),('K2_integral_dual_cuffs','K2 / Integral dual cuffs',5.6),('MK2_integral_dual_cuffs_3magnets','MK2 / Cuffs + magnets',5.6)]
for i,(name,title,scale) in enumerate(items):
    body=np.array(scene[name]['body']);off=np.array([0,21,0]) if i==0 else np.zeros(3)
    objects=[(body+off,(65,142,148))]
    if i==2:
        objects += [(np.array(t)+[0,0,5],(190,195,198)) for t in scene[name]['magnets']]
    im.paste(render(objects,530,450,scale),(i*550+10,175))
    text(i*550+30,145,title,27)
text(30,625,'68 × 126 × 16 mm',25)
text(580,625,'68 × 68 mm; 13.8 mm with pen',23)
text(1130,625,'68 × 68 mm; 13.8 mm with pen',23)
text(30,670,'Slide in through the upper guide.',22)
text(30,705,'Three magnets load from underneath.',22)
text(580,670,'Two cuffs and base print as one body.',22)
text(580,705,'No separate keyed pen collar.',22)
text(1130,670,'Three top-loading Ø6 × 2 pockets.',22)
text(1130,705,'Same integral cuffs as K2.',22)
text(40,755,'Fit-test prototypes: straps still needed for travel; retention and magnetic strength are unverified.',23)
im.save(OUT/'v3-three-designs.png')
# Separate underside illustration for the closed sheath's magnet assembly.
im=Image.new('RGB',(1150,720),(244,243,239));d=ImageDraw.Draw(im)
text(35,25,'S scabbard | underside magnet access',32)
body=np.array(scene['S_scabbard_3magnets']['body'])+[0,21,0]
im.paste(render([(body,(65,142,148))],600,550,4.2,rx=-132),(10,100))
text(640,155,'Each small socket:',26)
for j,line in enumerate(['1. Ø6 × 2 mm magnet against roof','2. Printed spacer, Ø6.05 × 2.3 mm','3. Bonded protective film underneath','Print the spacer file three times.','','Large ring recess = case attachment.','Small sockets = pen magnets.','','0.6 mm plastic roof separates','the magnets from the pen tunnel.']):text(640,210+j*36,line,20)
text(35,665,'Glue allowance: 0.1 mm nominal. Dry-fit the stack before bonding; no press-fit closure.',21)
im.save(OUT/'S-magnet-installation.png')
