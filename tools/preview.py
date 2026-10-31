"""contact sheet: 2 frames per beat for an episode → <ep>/preview.png (usage: python3 tools/preview.py epXX_name [w])"""
import sys, os, importlib.util
from PIL import Image, ImageDraw
ep = sys.argv[1]; K = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"; os.chdir(K + ep)
sys.argv = [sys.argv[0], "x.png"]
spec = importlib.util.spec_from_file_location("m", "render.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
EP, TL = m.EP, m.TL
ts = []
for k in EP.order:
    b = TL.T[k]; ts += [b["start"] + b["dur"] * .45, b["start"] + b["dur"] + .1]
ims = []
for t in ts:
    img = Image.new("RGB", (1080, 1920), m.BG); d = ImageDraw.Draw(img); EP.draw(img, d, t)
    ims.append(img.crop((0, 200, 1080, 1500)).resize((270, 325)))
cols = 6; rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 274, rows * 329), (60, 60, 60))
for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 274, (i // cols) * 329))
sheet.save("preview.png"); print("ok", ep)
