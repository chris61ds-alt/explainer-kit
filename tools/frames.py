import math, numpy as np
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920
def F(n, s): return ImageFont.truetype("../fonts/" + n, s)
BLK, BOLD, MONO = "Roboto-Black.woff", "Roboto-Bold.woff", "roboto-mono-latin-500.woff"
HEAD = [(120, 560), (110, 470), (80, 380), (70, 260), (100, 150), (170, 70), (270, 40), (360, 60), (420, 120), (440, 190), (445, 230),
        (470, 290), (505, 330), (470, 345), (468, 370), (482, 395), (466, 410), (480, 432), (460, 465), (430, 490), (380, 500), (350, 560)]
def frame(P, name):
    im = Image.new("RGB", (W, H), P["bg"]); d = ImageDraw.Draw(im)
    # header pill
    d.rounded_rectangle([60, 220, 470, 280], radius=30, fill=P["chip"]); d.text((90, 233), "NOT JUST YOU · 01", font=F(BOLD, 30), fill=P["chipfg"])
    # card
    d.rounded_rectangle([60, 320, 900, 1150], radius=48, fill=P["card"])
    # playful blobs
    for (x, y, r, c) in P["blobs"]: d.ellipse([x - r, y - r, x + r, y + r], fill=c)
    hx, hy, s = 170, 420, 1.15
    pts = [(hx + x * s, hy + y * s) for x, y in HEAD]
    d.polygon(pts + [(hx + 120 * s, hy + 560 * s)], fill=P["head"])
    ex, ey = hx + 235 * s, hy + 300 * s
    d.ellipse([ex - 30, ey - 44, ex + 30, ey + 44], fill=P["ear"])
    mx, my = hx + 470 * s, hy + 412 * s
    for i, r in enumerate((60, 110, 160)): d.arc([mx - r, my - r, mx + r, my + r], -45, 45, fill=P["air"], width=14)
    # bone wave
    x0, y0, x1, y1 = hx + 390 * s, hy + 470 * s, hx + 262 * s, hy + 305 * s
    wp = [(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k + math.sin(k * 9) * 20) for k in np.linspace(0, 1, 50)]
    d.line(wp, fill=P["bone"], width=16, joint="curve")
    d.rounded_rectangle([600, 360, 840, 420], radius=30, fill=P["air"]); d.text((720, 370), "AIR", font=F(BLK, 34), fill=P["onair"], anchor="ma")
    d.rounded_rectangle([110, 1040, 400, 1100], radius=30, fill=P["bone"]); d.text((255, 1050), "BONE", font=F(BLK, 34), fill=P["onbone"], anchor="ma")
    # subtitle
    d.text((70, 1220), "And once through", font=F(BLK, 76), fill=P["ink"]); d.text((70, 1310), "your own ", font=F(BLK, 76), fill=P["ink"])
    w = d.textlength("your own ", font=F(BLK, 76)); d.text((70 + w, 1310), "skull.", font=F(BLK, 76), fill=P["bone"])
    im.save(name, quality=90); return im
A = dict(bg=(238, 241, 246), card=(255, 255, 255), chip=(30, 34, 44), chipfg=(255, 255, 255), head=(66, 103, 245), ear=(40, 70, 200),
         air=(255, 196, 46), onair=(30, 34, 44), bone=(255, 98, 76), onbone=(255, 255, 255), ink=(30, 34, 44),
         blobs=[(840, 1080, 90, (255, 196, 46)), (120, 380, 40, (255, 98, 76)), (860, 520, 26, (66, 103, 245))])
B = dict(bg=(246, 242, 255), card=(234, 226, 255), chip=(103, 80, 164), chipfg=(255, 255, 255), head=(103, 80, 164), ear=(79, 55, 139),
         air=(125, 211, 176), onair=(10, 50, 40), bone=(239, 128, 160), onbone=(60, 10, 30), ink=(40, 30, 60),
         blobs=[(830, 1060, 110, (255, 216, 228)), (150, 400, 50, (205, 240, 225)), (870, 500, 30, (255, 216, 228))])
a, b = frame(A, "style_pop.jpg"), frame(B, "style_soft.jpg")
sh = Image.new("RGB", (W * 2 + 40, H), (60, 60, 60)); sh.paste(a, (0, 0)); sh.paste(b, (W + 40, 0))
sh.resize((sh.width // 2, sh.height // 2)).save("bright_styles.jpg", quality=88); print("ok")
