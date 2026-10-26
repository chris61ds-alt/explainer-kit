import os, numpy as np, soundfile as sf, subprocess
from kokoro_onnx import Kokoro
from PIL import Image, ImageDraw, ImageFont
K = os.path.expanduser("~/kokoro/"); k = Kokoro(K + "kokoro-v1.0.onnx", K + "voices-v1.0.bin")
LINE = "If you cringe at your own recorded voice, you're far from alone. Here's why."
VOICES = [("af_heart", "en-us", "A · warm, female, US"), ("af_bella", "en-us", "B · bright, female, US"),
          ("bf_emma", "en-gb", "C · friendly, female, UK"), ("am_puck", "en-us", "D · playful, male, US"),
          ("am_michael", "en-us", "E · friendly, male, US"), ("bm_george", "en-gb", "current · male, UK")]
SR = 24000; parts, marks, t = [], [], 0.0
for v, lang, label in VOICES:
    a, sr = k.create(LINE, voice=v, speed=1.05, lang=lang)
    idx = np.where(np.abs(a) > .01)[0]; a = a[idx[0]: idx[-1] + int(.1 * sr)]
    a = a / np.abs(a).max() * .8
    gap = np.zeros(int(.8 * sr)); marks.append((t, t + len(a) / sr + .8, label)); parts += [a, gap]; t += len(a) / sr + .8
audio = np.concatenate(parts); sf.write("voices.wav", audio, SR)
F = ImageFont.truetype("../fonts/Roboto-Black.woff", 96); M = ImageFont.truetype("../fonts/roboto-mono-latin-500.woff", 34)
W, H, FPS = 1080, 1920, 30
p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-i", "voices.wav", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "30", "-c:a", "aac", "-b:a", "160k", "-shortest", "voice_samples.mp4"], stdin=p_ if False else subprocess.PIPE)
frames = {}
for fr in range(int(t * FPS)):
    tt = fr / FPS; lab = next(l for a_, b_, l in marks if a_ <= tt < b_)
    if lab not in frames:
        im = Image.new("RGB", (W, H), (238, 241, 246)); d = ImageDraw.Draw(im)
        d.text((80, 300), "VOICE TEST", font=M, fill=(90, 100, 120))
        key, rest = lab.split(" · ", 1)
        d.text((80, 700), key, font=ImageFont.truetype("../fonts/Roboto-Black.woff", 260), fill=(66, 103, 245) if key != "current" else (150, 150, 150))
        d.text((80, 1000), rest, font=F, fill=(30, 34, 44))
        frames[lab] = np.array(im).tobytes()
    p.stdin.write(frames[lab])
p.stdin.close(); p.wait(); print("ok", round(t, 1))
