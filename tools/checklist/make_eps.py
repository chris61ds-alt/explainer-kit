"""Collects all episodes with media + schedule into eps.json and refreshes thumbs/ (run before build.py)."""
import json, glob, os, re
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(os.path.dirname(H)); os.chdir(K)
rows = json.load(open('publish/schedule.json')); hdr = rows[0]; plan = {int(r[2]): dict(zip(hdr, r)) for r in rows[1:]}
eps = []
os.makedirs(f'{H}/thumbs', exist_ok=True)
for d in sorted(glob.glob('ep[0-9][0-9]_*')):
    no = int(d[2:4])
    if not os.path.exists(f'publish/media/nj{no:02d}.mp4'): continue
    src = open(f'{d}/render.py').read()
    m = re.search(r'Episode\(TL, *\d+, *"([^"]+)"', src) or re.search(r'title *= *"([^"]+)"', src)
    title = m.group(1).upper() if m else d[5:].replace('_', ' ').upper()
    cap = plan[no]['caption'] if no in plan else open(f'{d}/caption.md').read().strip()
    eps.append(dict(no=no, title=title, caption=cap, date=plan.get(no, {}).get('date', ''), time=plan.get(no, {}).get('time', '')))
    t = f'{H}/thumbs/nj{no:02d}.jpg'
    if not os.path.exists(t):
        im = Image.open(f'publish/media/nj{no:02d}.jpg').convert('RGB'); im.thumbnail((180, 320)); im.save(t, quality=72)
json.dump(eps, open(f'{H}/eps.json', 'w'), ensure_ascii=False)
print(len(eps), 'episodes,', sum(1 for e in eps if e['date']), 'scheduled')
