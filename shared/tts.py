"""Synthesize every beat of ./script.json with Kokoro → vo/*.wav + vo/meta.json (+ proof.json with sources).
Style v3 (default since 31.10.2026, NJY_STYLE=v2 = old): intonation per beat — guess opener a bit faster; a reveal (beat after a "tease", or "reveal": true)
a bit slower, sentence by sentence with a short pause, so the number lands. A beat's own "speed" always wins."""
import json, os, re, numpy as np, soundfile as sf
import subprocess
V3 = os.environ.get("NJY_STYLE", "v3") == "v3"
s = json.load(open("script.json")); os.makedirs("vo", exist_ok=True); meta = []
# 22.11.2026: external voice (ElevenLabs A/B test). "voice": "ext:<folder>" -> <folder>/<beat id>.mp3 (made by publish/ElevenLabs.gs),
# only trimmed/squeezed here like Kokoro audio. Kokoro is not loaded then.
EXT = s["voice"][4:] if s["voice"].startswith("ext:") else None
# 26.11.2026: Kyutai Pocket TTS ("voice": "pocket:<name>", e.g. pocket:alba – model CC BY 4.0, voice alba CC BY 4.0 →
# caption credit "Voice: Kyutai Pocket TTS (alba), CC BY 4.0"). Model loaded once; no speed parameter → a beat's speed ≠ 1 is
# applied afterwards with ffmpeg atempo (pitch kept). SAY respellings were made for Kokoro/espeak: POCKET_SAY decides which
# of them still apply (see STIMME_UEBERGABE.md).
POCKET = s["voice"][7:] if s["voice"].startswith("pocket:") else None
if POCKET:
    from pocket_tts import TTSModel
    PM = TTSModel.load_model(); PSTATE = PM.get_state_for_audio_prompt(POCKET)
if not EXT and not POCKET:
    from kokoro_onnx import Kokoro
    K = os.path.expanduser("~/kokoro/"); k = Kokoro(K + "kokoro-v1.0.onnx", K + "voices-v1.0.bin")
def load_ext(bid, sr=44100):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(EXT, bid + ".mp3"), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64), sr

def voice_of(spec):
    """'af_heart' or a blend 'af_heart:0.5+af_bella:0.5' (since 02.11.2026 Dot = 50/50 heart + bella, a bit more cheerful)"""
    if "+" not in spec and ":" not in spec: return spec
    style = 0
    for part in spec.split("+"):
        name, w = (part.split(":") + ["1"])[:2]; style = style + float(w) * k.get_voice_style(name.strip())
    return style
VOICE = None if (EXT or POCKET) else voice_of(s["voice"])
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

# Pronunciation fixes (14.11.2026, Chris: "live" sounded like "life"): espeak reads the verb "live" as /laɪv/ after some words
# ("probably live closer"). Only the synthesized text is respelled; subtitles keep the original. "lives" (noun) stays /laɪvz/.
SAY = [(re.compile(r"\b([Ll])ive\b"), r"\1iv"),
       # 18.11.2026 (Chris: "lives on" sounded like "lifes"): the VERB "lives" before a preposition/adverb -> /lɪvz/
       (re.compile(r"\b([Ll])ives (on|in|with|at|near|alone|together|off|like|abroad|here|there)\b"), r"\1ivz \2"),
       # 26.11.2026: names the voice mangles ("Merer" came out as "Murr")
       (re.compile(r"\bMerer\b"), "Mehrer")]
POCKET_SAY = []            # tested 26.11.2026 (Whisper): alba reads 'live'/'lives on' right without respelling, and 'Merer' is
                          # closer to correct unchanged ('mirror') than respelled ('Mehrer' → 'Marr') → no respellings for alba
def say(p):
    for rx, rep in (POCKET_SAY if POCKET else SAY): p = rx.sub(rep, p)
    return p

def tempo(a, sr, f):
    """speed change without pitch change (ffmpeg atempo) – Pocket TTS has no speed parameter"""
    if abs(f - 1) < .005: return a
    raw = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-", "-af", f"atempo={f}", "-f", "f32le", "-"],
                         input=a.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)

def create(p, sp):
    """one sentence/beat → (audio, sr) with the configured engine"""
    if POCKET:
        a = PM.generate_audio(PSTATE, say(p)).numpy().astype(np.float64).squeeze(); sr = PM.sample_rate
        return tempo(a, sr, sp), sr
    return k.create(say(p), voice=VOICE, speed=sp, lang=s["lang"])

for b in s["beats"]:
    sp = b.get("speed") or (s["speed"] * (1.06 if b["id"] == "guess" else .94 if b["id"] in reveal else 1.0) if V3 else s["speed"])
    parts = [p for p in re.split(r"(?<=[.?!])\s+", b["text"]) if p]
    if EXT:
        a, sr = load_ext(b["id"]); a = squeeze(trim(a, sr), sr)
    elif POCKET and len(parts) > 1:                                # narrator pauses between sentences (Chris 26.11.2026)
        out = []; base = s.get("pause", .38)
        for j, p in enumerate(parts):
            a, sr = create(p, sp); out.append(squeeze(trim(a, sr, tail=.04), sr))
            if j < len(parts) - 1:
                short = len(p.split()) <= 3                         # 'Sails up.' / 'Gone.' -> a beat longer
                out.append(np.zeros(int((base + (.14 if short else 0) + (.08 if p.endswith("?") else 0)) * sr)))
        a = np.concatenate(out)
    elif V3 and (b["id"] in reveal or any(rising(p) for p in parts)):
        out = []; gap = .16 if b["id"] in reveal else .14
        for j, p in enumerate(parts):
            a, sr = create(p, sp); a = trim(a, sr, tail=.04)
            if rising(p): a = rise(a, sr)
            out.append(squeeze(a, sr))
            if j < len(parts) - 1: out.append(np.zeros(int(gap * sr)))
        a = np.concatenate(out)
    else:
        a, sr = create(b["text"], sp); a = squeeze(trim(a, sr), sr)
    f = int(.008 * sr); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
    sf.write(f"vo/{b['id']}.wav", a, sr); meta.append(dict(id=b["id"], text=b["text"], dur=len(a) / sr, sr=sr)); print(b["id"], round(len(a) / sr, 2))
json.dump(meta, open("vo/meta.json", "w"), indent=1); json.dump(dict(sources=s.get("sources", [])), open("proof.json", "w"), indent=1)
print("total", round(sum(m["dur"] for m in meta), 2))
