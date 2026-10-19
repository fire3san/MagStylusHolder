from render_common import *
scene = json.loads((OUT / 'scenes.json').read_text())
im = Image.new('RGB', (1500, 1050), (244, 243, 239))
d = ImageDraw.Draw(im)

def text(x, y, s, size=24):
    d.text((x, y), s, font=ImageFont.truetype(FONT, size), fill='#26383d')

text(40, 25, 'v5 | Shield scabbard + tunnel-through-clips K+M', 35)
for i, (name, title, scale) in enumerate([
    ('KM_tunnel_through_clips', 'K+M / Tunnel extends through all clips', 5.2),
    ('Shield_scabbard', 'Scabbard / Shield outline with border + ridge', 3.6),
]):
    v = np.array(scene[name])
    off = [0, 21, 0] if i else [0, 0, 0]
    im.paste(render([(v + off, (65, 142, 148))], 710, 440, scale), (i*750+15, 120))
    im.paste(render([(v + off, (65, 142, 148))], 710, 360, scale*.8, rx=-132), (i*750+15, 600))
    text(i*750+35, 100, title, 26)
    text(i*750+35, 570, 'Underside: three pen-magnet sockets', 23)

text(40, 980, 'No strap slots. Same bore/magnet dimensions as v4; decorative changes only.', 24)
im.save(OUT / 'v5-designs.png')
print("Saved v5-designs.png")
