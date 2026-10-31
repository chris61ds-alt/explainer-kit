"""Synthesize every beat of ./script.json with Kokoro → vo/*.wav + vo/meta.json (+ proof.json with sources).
NJY_STYLE=v3 (test): intonation per beat — guess opener a bit faster; a reveal (beat after a "tease", or "reveal": true)
a bit slower, sentence by sentence with a short pause, so the number lands. A beat's own "speed" always wins."""
import json, os, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
K = os.path.expanduser("~/kokoro/"); k = Kokoro(K + "kokoro-v1.0.onnx", K + "voices-v1.0.bin")
V3 = os.environ.get("NJY_STYLE") == "v3"
s = json.load(open("script.json")); os.makedirs("vo", exist_ok=True); meta = []
reveal = {s["beats"][i + 1]["id"] for i, b in enumerate(s["beats"][:-1]) if b.get("tease")} | {b["id"] for b in s["beats"] if b.get("reveal")}

def trim(a, sr, head=.03, tail=.08):
    idx = np.where(np.abs(a) > .01)[0]; return a[max(0, idx[0] - int(head * sr)): idx[-1] + int(tail * sr)].astype(np.float64)

for b in s["beats"]:
    sp = b.get("speed") or (s["speed"] * (1.06 if b["id"] == "guess" else .94 if b["id"] in reveal else 1.0) if V3 else s["speed"])
    if V3 and b["id"] in reveal:
        parts = [p for p in re.split(r"(?<=[.?!])\s+", b["text"]) if p]
        out = []
        for j, p in enumerate(parts):
            a, sr = k.create(p, voice=s["voice"], speed=sp, lang=s["lang"]); out.append(trim(a, sr, tail=.04))
            if j < len(parts) - 1: out.append(np.zeros(int(.16 * sr)))
        a = np.concatenate(out)
    else:
        a, sr = k.create(b["text"], voice=s["voice"], speed=sp, lang=s["lang"]); a = trim(a, sr)
    f = int(.008 * sr); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
    sf.write(f"vo/{b['id']}.wav", a, sr); meta.append(dict(id=b["id"], text=b["text"], dur=len(a) / sr, sr=sr)); print(b["id"], round(len(a) / sr, 2))
json.dump(meta, open("vo/meta.json", "w"), indent=1); json.dump(dict(sources=s.get("sources", [])), open("proof.json", "w"), indent=1)
print("total", round(sum(m["dur"] for m in meta), 2))
