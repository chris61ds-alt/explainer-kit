"""One command per episode:  python3 shared/build.py ep11_compliments
1. TTS (only if script.json changed)  2. ASR per beat on the voice files  3. render MP4
4. verify.py (spec, black frames, loudness, size)  5. ASR per beat on the FINAL mix (cut by the timeline, no 30 s window errors)
6. cover PNG  7. caption.md present?  → prints a short report and writes build_report.json"""
import sys, os, json, hashlib, subprocess, importlib.util, tempfile

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SH = os.path.join(KIT, "shared")
ep = os.path.abspath(sys.argv[1] if os.path.isabs(sys.argv[1]) else os.path.join(KIT, sys.argv[1]))
name = os.path.basename(ep); os.chdir(ep)
skip_render = "--no-render" in sys.argv
rep = {"episode": name}

def sh(cmd, **kw): return subprocess.run(cmd, shell=True, capture_output=True, text=True, **kw)

# 1 TTS ------------------------------------------------------------------------------------------
sc = json.load(open("script.json"))
h = hashlib.sha256(json.dumps([sc["voice"], sc["speed"], sc["lang"], sc["beats"], os.environ.get("NJY_STYLE", "v3")], sort_keys=True).encode()).hexdigest()[:16]
hf = os.path.join("vo", ".hash")
if not (os.path.exists(hf) and open(hf).read() == h):
    r = sh(f"python3 {SH}/tts.py"); print(r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr[-500:])
    os.makedirs("vo", exist_ok=True); open(hf, "w").write(h); rep["tts"] = "new"
else: rep["tts"] = "cached"

# 2 ASR on voice files ---------------------------------------------------------------------------
sys.path.insert(0, SH)
import asr_check as A, re
_n = A.norm
_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
def _words(n):
    if n < 20: return _ONES[n]
    if n < 100: return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    if n < 1000: return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + _words(n % 100))
    if n < 1000000: return _words(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + _words(n % 1000))
    return str(n)
def _clean(x):
    x = re.sub(r"[\[(][^\])]*[\])]?$|[\[(][^\])]*[\])]", " ", x)            # Whisper hallucinations like [BUZZER]
    x = re.sub(r"\$(\d[\d,]*)", lambda m: m.group(1) + " dollars", x)
    x = re.sub(r"(\d+)\s*%", lambda m: m.group(1) + " percent", x)
    x = re.sub(r"\d[\d,]*", lambda m: _words(int(m.group(0).replace(",", ""))), x)
    return x.replace("-", " ")
A.norm = lambda x: _n(_clean(x))
issues = []
for b in json.load(open("vo/meta.json")):
    hyp = A.transcribe(f"vo/{b['id']}.wav"); r_, h_ = A.norm(b["text"]), A.norm(hyp); e = A.wer(r_, h_)
    if e: issues.append((b["id"], e, len(r_), hyp.strip()))
rep["asr_voice"] = [f"{i}: {e}/{n} | {hyp}" for i, e, n, hyp in issues]

# 3 render ---------------------------------------------------------------------------------------
mp4 = f"{name}.mp4"
if not skip_render:
    r = sh(f"python3 render.py {mp4}")
    if r.returncode: print(r.stderr[-2000:]); sys.exit("render failed")
# 4 verify ---------------------------------------------------------------------------------------
r = sh(f"python3 {SH}/verify.py {mp4}"); rep["verify"] = "PASS" if "PASS" in r.stdout else "FAIL"
try: rep["verify_detail"] = json.loads(r.stdout[:r.stdout.rindex("}") + 1])
except Exception: rep["verify_detail"] = r.stdout[-800:]

# 5 ASR on the final mix, beat by beat --------------------------------------------------------------
spec = importlib.util.spec_from_file_location("render_mod", os.path.join(ep, "render.py"))
sys.argv = [sys.argv[0], "x.png"]; mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
TL = mod.TL; final = []
with tempfile.TemporaryDirectory() as td:
    for k, b in TL.T.items():
        if b.get("mute") or not b["text"]: continue
        w = os.path.join(td, k + ".wav")
        sh(f"ffmpeg -y -loglevel error -ss {max(0, b['start'] - .08):.2f} -t {b['dur'] + .3:.2f} -i {mp4} -ac 1 -ar 16000 {w}")
        hyp = A.transcribe(w); r_, h_ = A.norm(b["text"]), A.norm(hyp); e = A.wer(r_, h_)
        final.append((k, e, len(r_), hyp.strip()))
tot = sum(x[1] for x in final); n = sum(x[2] for x in final)
rep["asr_final_wer"] = f"{tot}/{n} = {tot / max(1, n):.1%}"
rep["asr_final_issues"] = [f"{k}: {e}/{m} | {hyp}" for k, e, m, hyp in final if e]
rep["duration_s"] = round(TL.total, 2)
if hasattr(mod, "EP") and hasattr(mod.EP, "calm"):
    rep["longest_calm_s"] = mod.EP.calm(getattr(mod, "FX", ()) + mod.EP.v2_fx())
    if rep["longest_calm_s"] > 3: print(f"  ⚠ longest calm stretch {rep['longest_calm_s']} s (> 3 s)")

# 6 cover ----------------------------------------------------------------------------------------
if hasattr(mod, "EP"): rep["cover"] = mod.EP.make_cover(f"{name}_cover.png")
# 7 caption --------------------------------------------------------------------------------------
rep["caption"] = "ok" if os.path.exists("caption.md") else "MISSING"

json.dump(rep, open("build_report.json", "w"), indent=1, ensure_ascii=False)
print(f"\n== {name} ==  {rep['duration_s']} s · verify {rep['verify']} · final ASR {rep['asr_final_wer']} · caption {rep['caption']}")
for x in rep["asr_voice"]: print("  voice:", x)
for x in rep["asr_final_issues"]: print("  final:", x)
