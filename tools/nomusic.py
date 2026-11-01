"""Version without music (voice + sound effects only) for trend sounds in the Instagram/TikTok app.
Reuses the finished video, only the audio is rebuilt:  python3 tools/nomusic.py ep86_singles [ep87_... ...]
→ epNN_x/epNN_x_nomusic.mp4"""
import sys, os, subprocess, importlib.util
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for e in sys.argv[1:]:
    ep = os.path.join(KIT, e); name = os.path.basename(ep.rstrip("/"))
    mp4, wav, out = (os.path.join(ep, name + s) for s in (".mp4", "_nomusic.wav", "_nomusic.mp4"))
    code = f"""
import sys, os, importlib.util
os.environ["NJY_STEM"] = "nomusic"; os.chdir({ep!r}); sys.path.insert(0, {os.path.join(KIT, 'shared')!r})
spec = importlib.util.spec_from_file_location("r", "render.py"); sys.argv = ["x", {wav!r}]
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
import swiss
EP = m.EP; swiss.MUSIC = dict(swiss.MUSIC, **EP.music)
extra = []
if swiss.MUSIC.get("audio", swiss.AUDIO) == "v5":                 # keep the counter runs (they are effects, not music)
    import sound5; extra = sound5.counter_runs(EP.counters(), 220.0 * 2 ** (swiss.MUSIC["root"] / 12))
swiss.build_audio(EP.TL, list(getattr(m, 'FX', [])) + EP.v2_fx() + extra, {wav!r})
"""
    subprocess.run([sys.executable, "-c", code], check=True, env=dict(os.environ, NJY_STEM="nomusic"))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp4, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.75:level=false", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(wav); print("ok", out)
