import json, soundfile as sf, numpy as np, os
from kokoro_onnx import Kokoro
K = os.path.expanduser("~/kokoro/")
k = Kokoro(K + "kokoro-v1.0.onnx", K + "voices-v1.0.bin")
s = json.load(open("script.json")); os.makedirs("vo", exist_ok=True)
meta = []
for b in s["beats"]:
    audio, sr = k.create(b["text"], voice=s["voice"], speed=s["speed"], lang=s["lang"])
    # trim leading/trailing silence
    idx = np.where(np.abs(audio) > 0.01)[0]
    audio = audio[max(0, idx[0] - int(.03 * sr)): idx[-1] + int(.08 * sr)]
    sf.write(f"vo/{b['id']}.wav", audio, sr)
    meta.append(dict(id=b["id"], text=b["text"], dur=len(audio) / sr, sr=sr))
    print(b["id"], round(len(audio) / sr, 2))
json.dump(meta, open("vo/meta.json", "w"), indent=1)
print("total", round(sum(m["dur"] for m in meta), 2))
