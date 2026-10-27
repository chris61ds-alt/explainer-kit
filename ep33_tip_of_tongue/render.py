"""NOT JUST YOU – No. 33: tip of the tongue (Brown & McNeill 1966; Schwartz 1999). Area: language."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from swiss import *

HERE = os.path.dirname(os.path.abspath(__file__))
TL = Timeline(HERE, lead=.15, gaps={"hook": .6, "study": .6, "name": .6, "langs": .6, "hint": .8, "end": 2.2})
S, E, cue = TL.S, TL.E, TL.cue
ORDER = ["hook", "study", "name", "langs", "hint", "end"]
EP = Episode(TL, 33, "TIP OF THE TONGUE", order=ORDER,
             chapters={"hook": "IT'S ON THE…", "study": "THE STUDY", "name": "IT'S IN THERE", "langs": "EVERYWHERE", "hint": "THE KEY"},
             sources=("Brown & McNeill (1966), J. Verbal Learning & Verbal", "Behavior 5 · Schwartz (1999), Psychon. Bull. Rev. 6"),
             music=dict(bpm=94, root=1, prog="warm", kick="half", gaps=[(E("hook") + .05, S("study") + .05)]),
             cover=dict(words=["IT'S ON", "THE TIP…"], kicker="Why words get stuck."))

THINK = {"arms": ((140, 220), (-10, -5))}
WORD = "GONDOLA"
def slots(d, x, y, revealed, size=96, gap=14, col=INK):
    for i, ch in enumerate(WORD):
        xx = x + i * (size + gap)
        d.line([xx, y + size, xx + size, y + size], fill=INK, width=6)
        if i in revealed: d.text((xx + size / 2, y + size / 2), ch, font=F(BLK, int(size * .9)), fill=col if i else SIG, anchor="mm")

def sc_hook(img, d, t):
    d.text((X0 - 6, 300), "IT'S ON", font=F(BLK, 180), fill=INK)
    d.text((X0, 480), "THE TIP…", font=F(BLK, 140), fill=SIG)
    h = picto(d, 330, FLOOR, 1.05, INK, pose=THINK)
    speech_box(d, 400, 690, 420, (t - .4) / .4, INK, 1, "it's on the tip of my…", 28)
    fig(d, "fig. 1 — you know it. you just can't say it.")

def sc_study(img, d, t):
    t0 = S("study"); fl = cue("study", "first letter"); sy = cue("study", "syllables")
    d.text((X0, 320), "DEFINITION:", font=F(BLK, 90), fill=INK)
    d.rectangle([X0, 440, X1, 600], outline=INK, width=4)
    d.text((X0 + 24, 480), "a long, narrow boat rowed", font=F(COND, 38), fill=INK); d.text((X0 + 24, 530), "through the canals of Venice", font=F(COND, 38), fill=INK)
    rev = set()
    if t >= fl: rev.add(0)
    slots(d, X0, 700, rev)
    if t >= fl: note(d, X0 + 48, 820, X0 + 200, 940, "first letter: known", (t - fl) / .35, SIG, size=28)
    if t >= sy:
        for i in range(3): d.ellipse([X0 + 560 + i * 80, 960, X0 + 600 + i * 80, 1000], fill=INK)
        d.text((X0 + 560, 1020), "3 syllables: known", font=F(COND, 28), fill=INK)
    fig(d, "classic method: rare-word definitions · Brown & McNeill, 1966 · example word ours")

def sc_name(img, d, t):
    t0 = S("name")
    words_in(d, t, [("IT'S IN", t0, 300, 170, INK), ("THERE.", t0 + .2, 470, 170, SIG)])
    slots(d, X0, 760, {0, 3})
    for i, (lab, x, y) in enumerate((("G…", X0, 960), ("3 syllables", X0 + 250, 1010), ("rhymes with…?", X0 + 520, 960))):
        k = ease((t - cue("name", "not all") + .3 - i * .2) / .3)
        if k > 0: box_label(d, x, y, lab, 28, WHITE, SIG if i == 0 else INK)
    fig(d, "fig. 2 — the pieces arrive, the whole word doesn't")

def sc_langs(img, d, t):
    t0 = S("langs"); fy = cue("langs", "forty-five")
    d.text((X0, 320), "45 OF 51", font=F(BLK, 160), fill=SIG)
    d.text((X0, 510), "languages have a phrase for it", font=F(COND, 34), fill=INK)
    for i in range(51):
        r, c = divmod(i, 17); x = X0 + c * 50; y = 600 + r * 50
        on = i < 45 and t >= fy - .2 and i < 45 * clamp((t - fy + .2) / .8)
        d.rectangle([x, y, x + 40, y + 40], fill=SIG if on else None, outline=INK, width=3)
    for i, (lang, phrase) in enumerate((("DE", "Es liegt mir auf der Zunge"), ("FR", "sur le bout de la langue"), ("ES", "en la punta de la lengua"))):
        k = ease((t - t0 - .6 - i * .4) / .3)
        if k > 0:
            y = 800 + i * 90; box_label(d, X0, y, lang, 28, WHITE, INK); d.text((X0 + 80, y), phrase, font=F(COND, 34), fill=INK)
    fig(d, "Schwartz, 1999")

def sc_hint(img, d, t):
    t0 = S("hint"); un = cue("hint", "unlocks")
    d.text((X0, 320), "A HINT:", font=F(BLK, 130), fill=INK)
    box_label(d, X0, 490, '"go…"', 60, WHITE, SIG)
    k = clamp((t - un + .2) / .6)
    slots(d, X0, 700, set(range(int(len(WORD) * k) + 1)) if t >= un - .2 else {0})
    h = picto(d, 760, FLOOR, .7, INK, pose=OPEN if k >= 1 else THINK)
    fig(d, "a first sound often unlocks the whole word")

EP.scenes = {"hook": sc_hook, "study": sc_study, "name": sc_name, "langs": sc_langs, "hint": sc_hint}
FX = [(0.0, thud(.5), 0), (.4, pop(.15), .2), *EP.cut_fx(), (S("study") + .05, thud(.45), 0), (cue("study", "first letter"), pop(.2), -.2),
      (cue("study", "syllables"), pop(.15), .2), (cue("name", "not all"), whoosh(.5, .08), 0), (cue("langs", "forty-five"), thud(.45), 0),
      *[(S("langs") + .6 + i * .4, pop(.12), (i - 1) / 2) for i in range(3)], (cue("hint", "unlocks"), riser(.5, .08), 0),
      (cue("hint", "unlocks") + .4, pop(.25), 0), (S("end"), thud(.5), 0)]
if __name__ == "__main__": EP.run(FX)
