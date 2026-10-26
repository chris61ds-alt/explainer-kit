import json, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
K = os.path.expanduser("~/kokoro/"); k = Kokoro(K + "kokoro-v1.0.onnx", K + "voices-v1.0.bin")
s = json.load(open("script.json")); meta = []
for b in s["beats"]:
    a, sr = k.create(b["text"], voice=s["voice"], speed=s["speed"], lang=s["lang"])
    idx = np.where(np.abs(a) > .01)[0]; a = a[max(0, idx[0] - int(.03 * sr)): idx[-1] + int(.08 * sr)].astype(np.float64)
    f = int(.008 * sr); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
    sf.write(f"vo/{b['id']}.wav", a, sr); meta.append(dict(id=b["id"], text=b["text"], dur=len(a) / sr, sr=sr)); print(b["id"], round(len(a) / sr, 2))
json.dump(meta, open("vo/meta.json", "w"), indent=1); json.dump(dict(sources=s["sources"]), open("proof.json", "w"), indent=1)
print("total", round(sum(m["dur"] for m in meta), 2))
