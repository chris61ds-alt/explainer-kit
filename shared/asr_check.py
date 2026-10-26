"""Independent ASR (Whisper base.en via sherpa-onnx) + normalized WER against the script."""
import sys, json, re, os, numpy as np, soundfile as sf, sherpa_onnx
from scipy.signal import resample_poly
D = os.path.expanduser("~/asr/sherpa-onnx-whisper-base.en/")
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=D + "base.en-encoder.int8.onnx", decoder=D + "base.en-decoder.int8.onnx",
                                                 tokens=D + "base.en-tokens.txt", language="en", task="transcribe")
NUM = {"1": "one", "2": "two", "3": "three", "10,000": "ten thousand", "10000": "ten thousand", "50": "fifty"}
def norm(t):
    t = t.lower().replace("fifty-fifty", "fifty fifty").replace("50-50", "fifty fifty").replace("50/50", "fifty fifty")
    for k, v in NUM.items(): t = re.sub(rf"\b{k}\b", v, t)
    t = t.replace("’", "'").replace("recognize", "recognise"); t = re.sub(r"[^a-z' ]", " ", t)
    return t.split()
def wer(r, h):
    d = np.zeros((len(r) + 1, len(h) + 1), int); d[:, 0] = range(len(r) + 1); d[0, :] = range(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (r[i - 1] != h[j - 1]))
    return d[-1, -1]
def transcribe(path):
    a, sr = sf.read(path, dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    if sr != 16000: a = resample_poly(a, 16000, sr).astype("float32")
    out = []
    for s in range(0, len(a), 16000 * 25):   # whisper 30 s window
        st = rec.create_stream(); st.accept_waveform(16000, a[s:s + 16000 * 25]); rec.decode_stream(st); out.append(st.result.text)
    return " ".join(out)
if __name__ == "__main__":
    ref_all, hyp_all = [], []
    if len(sys.argv) > 1:   # whole file vs whole script
        ref = " ".join(b["text"] for b in json.load(open("script.json"))["beats"]); hyp = transcribe(sys.argv[1])
        r, h = norm(ref), norm(hyp); e = wer(r, h)
        print("HYP:", hyp); print(f"WER {e}/{len(r)} = {e / len(r):.1%}"); sys.exit()
    for b in json.load(open("vo/meta.json")):
        hyp = transcribe(f"vo/{b['id']}.wav"); r, h = norm(b["text"]), norm(hyp); e = wer(r, h)
        ref_all += r; hyp_all += h
        print(f"{b['id']:7s} err {e}/{len(r)} | {hyp.strip()}")
    e = wer(ref_all, hyp_all); print(f"TOTAL WER {e}/{len(ref_all)} = {e / len(ref_all):.1%}")
