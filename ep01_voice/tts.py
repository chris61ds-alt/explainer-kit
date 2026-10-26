"""Synthesize every beat; apply the two acoustic paths for the demo beats; write vo/*.wav + meta.json + proof.json."""
import json, os, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
from kokoro_onnx import Kokoro
K = os.path.expanduser("~/kokoro/")
k = Kokoro(K + "kokoro-v1.0.onnx", K + "voices-v1.0.bin")
s = json.load(open("script.json"))
def sos(kind, fc, sr, order=2): return butter(order, fc, kind, fs=sr, output="sos")
def inside(a, sr):   # model of the extra bone path: low band (<500 Hz) added on top, slight top-end roll-off
    low = sosfilt(sos("lowpass", 500, sr), a)
    return sosfilt(sos("lowpass", 7000, sr), a + 1.6 * low)
def rec(a, sr):      # air path only, as a phone mic would capture it: thinner lows
    return sosfilt(sos("highpass", 260, sr, 3), a)
def band_db(a, sr, lo, hi):
    f = np.fft.rfftfreq(len(a), 1 / sr); P = np.abs(np.fft.rfft(a)) ** 2
    return 10 * np.log10(P[(f >= lo) & (f < hi)].sum() + 1e-12)
def centroid(a, sr):
    f = np.fft.rfftfreq(len(a), 1 / sr); P = np.abs(np.fft.rfft(a)); return float((f * P).sum() / P.sum())
meta, proof = [], {}
for b in s["beats"]:
    a, sr = k.create(b["text"], voice=s["voice"], speed=s["speed"], lang=s["lang"])
    a = a.astype(np.float64)
    idx = np.where(np.abs(a) > .01)[0]; a = a[max(0, idx[0] - int(.03 * sr)): idx[-1] + int(.08 * sr)]
    if b["id"] == "demo_in":
        raw = a.copy()
        A, R = inside(raw, sr), rec(raw, sr)
        A *= np.abs(raw).max() / np.abs(A).max(); R *= np.abs(raw).max() / np.abs(R).max()
        proof = dict(model="inside = air + 1.6 x (lowpass 500 Hz), lowpass 7 kHz; recording = highpass 260 Hz (3rd order)",
                     low_band_db_difference=round((band_db(A, sr, 60, 500) - band_db(A, sr, 500, 4000)) - (band_db(R, sr, 60, 500) - band_db(R, sr, 500, 4000)), 1),
                     centroid_inside_hz=round(centroid(A, sr)), centroid_recording_hz=round(centroid(R, sr)),
                     spectrum_inside=[], spectrum_recording=[])
        # 24 log-spaced bands for the on-screen spectrum (real measurement of the two demo files)
        edges = np.geomspace(60, 8000, 25)
        for name, sig in (("spectrum_inside", A), ("spectrum_recording", R)):
            proof[name] = [round(band_db(sig, sr, edges[i], edges[i + 1]), 2) for i in range(24)]
        proof["band_edges_hz"] = [round(e) for e in edges]
    if b.get("fx") == "inside": a = inside(a, sr); a *= .95 / np.abs(a).max()
    if b.get("fx") == "rec": a = rec(a, sr); a *= .95 / np.abs(a).max()
    fade = int(.008 * sr); a[:fade] *= np.linspace(0, 1, fade); a[-fade:] *= np.linspace(1, 0, fade)
    sf.write(f"vo/{b['id']}.wav", a, sr)
    meta.append(dict(id=b["id"], text=b["text"], dur=len(a) / sr, sr=sr, fx=b.get("fx")))
    print(b["id"], round(len(a) / sr, 2))
json.dump(meta, open("vo/meta.json", "w"), indent=1)
proof["sources"] = s["sources"]; json.dump(proof, open("proof.json", "w"), indent=1)
print("total", round(sum(m["dur"] for m in meta), 2))
print({k_: v for k_, v in proof.items() if not k_.startswith("spectrum") and k_ != "sources"})
