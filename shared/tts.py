"""Synthesize every beat of ./script.json with Kokoro → vo/*.wav + vo/meta.json (+ proof.json with sources).
Style v3 (default since 31.10.2026, NJY_STYLE=v2 = old): intonation per beat — guess opener a bit faster; a reveal (beat after a "tease", or "reveal": true)
a bit slower, sentence by sentence with a short pause, so the number lands. A beat's own "speed" always wins."""
import json, os, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
K = os.path.expanduser("~/kokoro/"); k = Kokoro(K + "kokoro-v1.0.onnx", K + "voices-v1.0.bin")
V3 = os.environ.get("NJY_STYLE", "v3") == "v3"
s = json.load(open("script.json")); os.makedirs("vo", exist_ok=True); meta = []

def voice_of(spec):
    """'af_heart' or a blend 'af_heart:0.5+af_bella:0.5' (since 02.11.2026 Dot = 50/50 heart + bella, a bit more cheerful)"""
    if "+" not in spec and ":" not in spec: return spec
    style = 0
    for part in spec.split("+"):
        name, w = (part.split(":") + ["1"])[:2]; style = style + float(w) * k.get_voice_style(name.strip())
    return style
VOICE = voice_of(s["voice"])
reveal = {s["beats"][i + 1]["id"] for i, b in enumerate(s["beats"][:-1]) if b.get("tease")} | {b["id"] for b in s["beats"] if b.get("reveal")}

MAX_PAUSE = .15        # since 02.11.2026: pauses inside a beat (after "?", "!", ":") are capped – the sentence keeps flowing;
                       # the breathing room goes between beats instead (see cute.Timeline, tight pace)

def squeeze(a, sr, max_pause=MAX_PAUSE, thr=.012):
    """shorten every internal silence longer than max_pause to max_pause (cut out of its middle)"""
    win = max(1, int(.01 * sr)); env = np.convolve(np.abs(a), np.ones(win) / win, "same"); quiet = env < thr
    out, i, n, last = [], 0, len(a), 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]: j += 1
            if i > 0 and j < n and (j - i) > max_pause * sr:
                keep = int(max_pause * sr / 2); out.append(a[last:i + keep]); last = j - keep
            i = j
        else: i += 1
    out.append(a[last:]); return np.concatenate(out)

def trim(a, sr, head=.03, tail=.08):
    idx = np.where(np.abs(a) > .01)[0]; return a[max(0, idx[0] - int(head * sr)): idx[-1] + int(tail * sr)].astype(np.float64)

# Question rise (since 05.11.2026, variant "C", env NJY_QRISE=0 = off): Kokoro ends every question falling (−2…−4 semitones),
# so yes/no and fragment questions ("And men?", "Did it work?") sounded like statements. Each such question is synthesized
# as its own sentence and the pitch of its last 0.34 s is lifted by up to QRISE_ST semitones (WORLD resynthesis of the
# tail only, spectral envelope kept). Questions with a wh-word ("How did you meet?") and "Or …?" keep their natural fall.
QRISE = os.environ.get("NJY_QRISE", "1") == "1"; QRISE_ST, QRISE_DUR = 12.0, .34
WH = re.compile(r"\b(what|who|whom|whose|how|why|which|where|when)\b|^or\b", re.I)
def rising(p): return QRISE and p.rstrip().endswith("?") and not WH.search(p)

def rise(a, sr, st=QRISE_ST, dur=QRISE_DUR):
    import pyworld as pw
    f0, t = pw.harvest(a, sr, f0_floor=120, f0_ceil=500, frame_period=5); sp_ = pw.cheaptrick(a, f0, t, sr); ap = pw.d4c(a, f0, t, sr)
    vi = np.where(f0 > 0)[0]
    if len(vi) < 10: return a
    t0 = t[vi[-1]] - dur
    f2 = f0 * 2 ** (np.clip((t - t0) / dur, 0, 1) ** 1.6 * st / 12)          # ease-in ramp up to +st at the very end
    y = pw.synthesize(f2, sp_, ap, sr, frame_period=5)[:len(a)]
    if len(y) < len(a): y = np.pad(y, (0, len(a) - len(y)))
    s0 = max(0, int((t0 - .04) * sr)); x = int(.03 * sr); out = a.copy(); w = np.linspace(0, 1, x)
    out[s0:s0 + x] = a[s0:s0 + x] * (1 - w) + y[s0:s0 + x] * w; out[s0 + x:] = y[s0 + x:]       # 30 ms crossfade into the resynth
    pk, pk2 = np.max(np.abs(a[s0:])) + 1e-9, np.max(np.abs(out[s0:]))      # the resynth can overshoot → keep the original peak
    if pk2 > pk: out[s0:] *= pk / pk2                                       # (else the final mix fails true peak ≤ −1 dBTP)
    return out

for b in s["beats"]:
    sp = b.get("speed") or (s["speed"] * (1.06 if b["id"] == "guess" else .94 if b["id"] in reveal else 1.0) if V3 else s["speed"])
    parts = [p for p in re.split(r"(?<=[.?!])\s+", b["text"]) if p]
    if V3 and (b["id"] in reveal or any(rising(p) for p in parts)):
        out = []; gap = .16 if b["id"] in reveal else .14
        for j, p in enumerate(parts):
            a, sr = k.create(p, voice=VOICE, speed=sp, lang=s["lang"]); a = trim(a, sr, tail=.04)
            if rising(p): a = rise(a, sr)
            out.append(squeeze(a, sr))
            if j < len(parts) - 1: out.append(np.zeros(int(gap * sr)))
        a = np.concatenate(out)
    else:
        a, sr = k.create(b["text"], voice=VOICE, speed=sp, lang=s["lang"]); a = squeeze(trim(a, sr), sr)
    f = int(.008 * sr); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
    sf.write(f"vo/{b['id']}.wav", a, sr); meta.append(dict(id=b["id"], text=b["text"], dur=len(a) / sr, sr=sr)); print(b["id"], round(len(a) / sr, 2))
json.dump(meta, open("vo/meta.json", "w"), indent=1); json.dump(dict(sources=s.get("sources", [])), open("proof.json", "w"), indent=1)
print("total", round(sum(m["dur"] for m in meta), 2))
