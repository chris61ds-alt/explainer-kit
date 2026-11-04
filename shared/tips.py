"""Tips-format kit (04.11.2026, from No. 96/97): two fixed figures YOU + PARTNER, speech bubbles, hearts, tip headlines,
bookmark (save), isometric props (sofa, kitchen table + timer, café table, cube stacks) + iso hook (parts drop in, counter)
and iso recap (tips as numbered call-outs).

    from tips import *
    sc_hook = iso_hook(TL, "hook", I, sofa, ["3 TIPS."], "backed by research", save="Save this")
"""
import math
from thread import *
from iso import Iso, drop, callout, parts_counter, TOP, LEFT, RIGHT

YOU, PARTNER, BS = (290, 950), (670, 950), .34
def bust_box(x, y, s): return (int(x - 160 * s / .32), int(y - 110 * s / .32), int(x + 160 * s / .32), int(y + 160 * s / .32))

def couple(img, d, k=1.0, partner_col=MID, labels=None, you=YOU, partner=PARTNER, s=BS):
    silhouette(img, lambda m: front_bust(m, *you, s, 255), bust_box(*you, s), INK, cell=8, k=k)
    silhouette(img, lambda m: front_bust(m, *partner, s, 255), bust_box(*partner, s), partner_col, cell=8, k=k)
    if k > .6 and labels:
        d.text((you[0], 1104), labels[0], font=F(BLK, 26), fill=INK, anchor="ma"); d.text((partner[0], 1104), labels[1], font=F(BLK, 26), fill=partner_col, anchor="ma")

def bubble(d, who, text, k, col=INK, y=700, size=34, x=None):
    """speech bubble above YOU ('you') or PARTNER ('partner'), pops in with k → its box"""
    if k <= 0: return None
    f = F(BLK, size); w = d.textlength(text, font=f) + 44; h = size + 30
    sx = x if x is not None else (YOU if who == "you" else PARTNER)[0]
    x0 = min(max(X0, sx - w / 2), X1 - w); s = back(clamp(k)); cx, cy = x0 + w / 2, y + h / 2
    d.rounded_rectangle([cx - w / 2 * s, cy - h / 2 * s, cx + w / 2 * s, cy + h / 2 * s], radius=int(h / 2 * s), fill=col)
    d.polygon([(sx - 14 * s, y + h * s - 2), (sx + 14 * s, y + h * s - 2), (sx, y + h * s + 26 * s)], fill=col)
    if s > .6: d.text((cx, cy), text, font=F(BLK, int(size * min(1, s))), fill=BG, anchor="mm")
    return (x0, y, x0 + w, y + h)

def strike(d, box, k, col=INK):
    if box and k > 0: y = (box[1] + box[3]) / 2; d.line([box[0] - 8, y, lerp(box[0] - 8, box[2] + 8, ease(clamp(k))), y], fill=col, width=8)

def heart(d, cx, cy, r, col):
    d.ellipse([cx - r, cy - r * .9, cx, cy + r * .1], fill=col); d.ellipse([cx, cy - r * .9, cx + r, cy + r * .1], fill=col)
    d.polygon([(cx - r * .97, cy - r * .25), (cx + r * .97, cy - r * .25), (cx, cy + r * 1.05)], fill=col)

def tip_head(d, t, n, lines, t0, size=100):
    box_label(d, X0, 300, f"TIP {n}", 40, WHITE, INK, font=BLK)
    words_in(d, t, [(l, t0 + .1 + i * .15, 370 + i * size, size, INK) for i, l in enumerate(lines)])

def bookmark(d, t, ts, bx=X1 - 50, by=560):
    if t < ts: return
    k = back(clamp((t - ts) / .3))
    d.polygon([(bx - 40 * k, by - 56 * k), (bx + 40 * k, by - 56 * k), (bx + 40 * k, by + 56 * k), (bx, by + 28 * k), (bx - 40 * k, by + 56 * k)], fill=INK)
    if k > .7: d.text((bx - 60, by), "SAVE", font=F(MONO, 30), fill=INK, anchor="rm")

def clock(d, cx, cy, r, k, col=INK, label=None):
    """timer dial: arc fills with k"""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=8)
    if k > 0: d.pieslice([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14], -90, -90 + 360 * clamp(k), fill=col)
    if label: d.text((cx, cy + r + 18), label, font=F(MONO, 30), fill=col, anchor="ma")

# ---------------------------------------------------------------- isometric props: each returns {anchor: (x, y, z)} · T = drop-in times
def _T(T, n): return T or [-9] * n

def sofa(I, d, t, T=None):
    T = _T(T, 7)
    v, dz = drop(t, T[6])                                                                                 # side table with a mug (behind, right)
    if v: I.cyl(d, 380, -170, 0 + dz, 40, 110); I.cyl(d, 380, -170, 110 + dz, 70, 8); I.cyl(d, 380, -170, 118 + dz, 22, 34)
    for i, (x, y, z, a, b, h) in enumerate(((-260, -110, 0, 520, 220, 70), (-260, -110, 70, 520, 70, 150),   # base, backrest
                                           (-260, -40, 70, 60, 150, 90), (200, -40, 70, 60, 150, 90),       # armrests
                                           (-200, -40, 70, 200, 150, 30), (0, -40, 70, 200, 150, 30))):    # cushions
        v, dz = drop(t, T[i])
        if v: I.box(d, x, y, z + dz, a, b, h)
    return {"left": (-100, 35, 100), "right": (100, 35, 100), "back": (0, -75, 220), "arm": (230, 35, 160), "mug": (380, -170, 152)}

def kitchen_table(I, d, t, T=None, timer_col=TOP):
    T = _T(T, 7)
    for i, (x, y) in enumerate(((-230, -130), (190, -130), (-230, 90), (190, 90))):                      # legs
        v, dz = drop(t, T[0] if i < 2 else T[1])
        if v: I.box(d, x, y, dz, 40, 40, 190)
    v, dz = drop(t, T[2])
    if v: I.box(d, -260, -160, 190 + dz, 520, 300, 22)                                                    # table top
    for j, (x, y) in enumerate(((-150, 40), (130, -60))):                                                 # two mugs
        v, dz = drop(t, T[3 + j])
        if v: I.cyl(d, x, y, 212 + dz, 34, 50); cx, cy = I.P(x, y, 262 + dz); d.ellipse([cx - 18, cy - 8, cx + 18, cy + 8], fill=(120, 84, 60))
    v, dz = drop(t, T[5])
    if v: I.cyl(d, 0, -110, 212 + dz, 42, 30, top=timer_col); px, py = I.P(0, -110, 242 + dz); d.line([px, py, px + 14, py - 10], fill=INK, width=5)   # kitchen timer
    v, dz = drop(t, T[6])
    if v: I.box(d, 40, 30, 212 + dz, 120, 80, 6)                                                          # a note
    return {"you": (-150, 40, 262), "them": (130, -60, 262), "timer": (0, -110, 242), "note": (100, 70, 218), "top": (0, 0, 212)}

def bed(I, d, t, T=None, lamp_col=TOP):
    T = _T(T, 7)
    v, dz = drop(t, T[0])
    if v: I.box(d, 300, -330, dz, 120, 120, 120); I.cyl(d, 360, -270, 120 + dz, 26, 60); I.cyl(d, 360, -270, 180 + dz, 50, 40, top=lamp_col)   # nightstand + lamp
    for i, (x, y, z, a, b, h) in enumerate(((-260, -300, 0, 500, 40, 230),                               # headboard
                                           (-260, -260, 0, 500, 560, 80), (-250, -250, 80, 480, 540, 50))):  # frame, mattress
        v, dz = drop(t, T[1 + i])
        if v: I.box(d, x, y, z + dz, a, b, h)
    for j, x in enumerate((-220, 10)):                                                                     # two pillows
        v, dz = drop(t, T[4 + j])
        if v: I.box(d, x, -235, 130 + dz, 190, 110, 30)
    v, dz = drop(t, T[6])
    if v: I.box(d, -255, -90, 130 + dz, 490, 385, 18)                                                     # blanket
    return {"lamp": (360, -270, 220), "pillow_l": (-125, -180, 160), "pillow_r": (105, -180, 160), "blanket": (0, 100, 148), "stand": (360, -270, 120)}

def cube_stack(I, d, t, x0, y0, n, t0=-9, step=.05, size=56, top=TOP, gap=4):
    """n cubes stacked in a 2×2 footprint, dropping in one by one from t0 → top anchor"""
    s = size + gap; slots = [(0, 0), (s, 0), (0, s), (s, s)]
    for i in range(n):
        lx, ly = slots[(i % 4) if (i // 4) % 2 == 0 else (3 - i % 4)]
        v, dz = drop(t, t0 + i * step, h=90, dur=.2)
        if v: I.box(d, x0 + lx, y0 + ly, (i // 4) * size + dz, size, size, size, top=top)
    return (x0 + s / 2 + size / 2, y0 + s / 2 + size / 2, ((n - 1) // 4 + 1) * size)

# ---------------------------------------------------------------- iso scenes
def iso_hook(TL, key, I, prop, lines, sub=None, sub_cue=None, save=None, n_parts=7, figtxt="fig. 1 — schematic", size=150):
    """hook: the prop assembles part by part (counter), headline + optional sub line + bookmark at the 'save' cue"""
    def sc(img, d, t):
        t0 = TL.S(key); PT = [t0 + .15 + i * .22 for i in range(n_parts)]
        I.grid(img); I.shadow(d, 0, 0, 260, k=clamp((t - PT[0]) / .3)); prop(I, d, t, PT)
        words_in(d, t, [(l, t0 + .05 + i * .12, 320 + i * size, size, INK) for i, l in enumerate(lines)])
        if sub:
            tb = TL.cue(key, sub_cue) - .1 if sub_cue else t0 + .3; yb = 320 + len(lines) * size + 20
            if t >= tb: d.text((X0 + 4 - (1 - ease((t - tb) / .25)) * 40, yb), sub, font=F(COND, 50), fill=mix(BG, INK, ease((t - tb) / .25)))
        parts_counter(d, X1, 330, sum(t >= x for x in PT), n_parts)
        if save: bookmark(d, t, TL.cue(key, save) - .1)
        fig(d, figtxt)
    return sc

def iso_recap(TL, key, I, prop, title, items, figtxt="fig. 2 — save it"):
    """recap: the finished prop + one numbered call-out per tip, each on its cue · items = [(anchor, side, dy, label, col, cue)]"""
    def sc(img, d, t):
        t0 = TL.S(key); I.grid(img); I.shadow(d, 0, 0, 260); A = prop(I, d, t)
        words_in(d, t, [(title, t0 + .05, 320, 130, INK)])
        for n, (a, side, dy, label, col, cue_) in enumerate(items, 1):
            p = I.P(*A[a]); tc = TL.cue(key, cue_) - .15
            callout(d, p, side, p[1] + dy, n, label, col, k=(t - tc) / .4)
        fig(d, figtxt)
    return sc

def iso_fx(TL, key, n_parts=7):
    t0 = TL.S(key); return [(t0 + .15 + i * .22 + .2, tick(.05), (i % 5 - 2) / 3) for i in range(n_parts)]
