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

for b in s["beats"]:
    sp = b.get("speed") or (s["speed"] * (1.06 if b["id"] == "guess" else .94 if b["id"] in reveal else 1.0) if V3 else s["speed"])
    if V3 and b["id"] in reveal:
        parts = [p for p in re.split(r"(?<=[.?!])\s+", b["text"]) if p]
        out = []
        for j, p in enumerate(parts):
            a, sr = k.create(p, voice=VOICE, speed=sp, lang=s["lang"]); out.append(squeeze(trim(a, sr, tail=.04), sr))
            if j < len(parts) - 1: out.append(np.zeros(int(.16 * sr)))
        a = np.concatenate(out)
    else:
        a, sr = k.create(b["text"], voice=VOICE, speed=sp, lang=s["lang"]); a = squeeze(trim(a, sr), sr)
    f = int(.008 * sr); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
    sf.write(f"vo/{b['id']}.wav", a, sr); meta.append(dict(id=b["id"], text=b["text"], dur=len(a) / sr, sr=sr)); print(b["id"], round(len(a) / sr, 2))
json.dump(meta, open("vo/meta.json", "w"), indent=1); json.dump(dict(sources=s.get("sources", [])), open("proof.json", "w"), indent=1)
print("total", round(sum(m["dur"] for m in meta), 2))
