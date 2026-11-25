"""Automatic rule check (25.11.2026, after Chris noticed rules being forgotten). Checks the ⚙ rules of REGELN.md on the
finished episode. Used by build.py; standalone: python3 shared/rulecheck.py epXX_name"""
import os, re, sys, json, subprocess
import numpy as np

LEN = {"standard": (24, 32), "stand": (24, 32), "cliche": (24, 32), "map": (24, 32), "riddle": (24, 34), "pour": (24, 34), "race": (24, 40)}
DARK_OK = {"race"}                     # race: provisional, Chris has not decided yet (25.11.2026)
BAND = (470, 1180)


def motion(mp4, total):
    """per-frame mean abs difference inside the object band (10 fps, 270 px wide, grey)"""
    h = (BAND[1] - BAND[0]) // 4
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-vf", f"fps=10,crop=1080:{BAND[1] - BAND[0]}:0:{BAND[0]},scale=270:{h},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    F = np.frombuffer(raw, np.uint8).reshape(-1, h, 270).astype(np.float32)
    return np.abs(np.diff(F, axis=0)).mean(axis=(1, 2))


def check(ep, mp4, TL):
    s = json.load(open(os.path.join(ep, "script.json"))); src = open(os.path.join(ep, "render.py")).read()
    cap = open(os.path.join(ep, "caption.md")).read() if os.path.exists(os.path.join(ep, "caption.md")) else ""
    kind = s.get("kind"); beats = {b["id"]: b for b in s["beats"]}; out = []
    def r(n, ok, msg): out.append((n, bool(ok), msg))
    r("E kind", kind in LEN, f"kind = {kind!r} (standard/stand/cliche/riddle/pour/race/map)")
    r("1 sources", len(s.get("sources", [])) > 0, "sources in script.json")
    hook = beats.get("hook", {}).get("text", "")
    r("4 hook says you", re.search(r"\byour?\b", hook, re.I), f"hook: {hook[:60]}")
    for k, b in beats.items():
        if b.get("key"):
            ks = list(TL.T); i = ks.index(k)
            if i + 1 < len(ks):
                gap = TL.T[ks[i + 1]]["start"] - (TL.T[k]["start"] + TL.T[k]["dur"])
                r("7 pause after key", gap >= .75, f"{k}: {gap:.2f} s (≥ 0.8)")
    r("7 key beat marked", any(b.get("key") for b in s["beats"]), 'one beat with "key": true')
    r("9 end beat", beats.get("end", {}).get("text", "").strip() == "Not just you.", "last beat 'end' = Not just you.")
    lo, hi = LEN.get(kind, (24, 32))
    r("10 length", lo <= TL.total <= hi, f"{TL.total:.1f} s (allowed {lo}–{hi} s for {kind})")
    m = motion(mp4, TL.total)
    r("11 motion from frame 0", m[:5].max() > 1.0, f"max change in the first 0.5 s: {m[:5].max():.2f}")
    still, best, at, end = 0, 0, 0, int((TL.total - 1.0) * 10)
    for i, v in enumerate(m[:end]):
        still = still + 1 if v < .35 else 0
        if still > best: best, at = still, (i - still + 1) / 10
    r("13 nothing stands still", best / 10 <= 1.5, f"longest still stretch {best / 10:.1f} s at {at:.1f} s (≤ 1.5 s)")
    r("14 camera at the payoff", "camera(" in src or "payoff_cam(" in src, "fx2.camera / stand.payoff_cam in render.py")
    r("16 look", kind in DARK_OK or ("light_look(" in src and ("shadowed(" in src or "ep=EP" in src)), "light look + shadows (dark only for race, provisional)")
    r("18 caption", cap and "#" not in cap and "👇" in cap and "Source:" in cap, "no hashtags · question + 👇 · Source:")
    return out


if __name__ == "__main__":
    import importlib.util
    ep = os.path.abspath(sys.argv[1]); name = os.path.basename(ep); sys.path.insert(0, os.path.join(ep, "..", "shared")); os.chdir(ep)
    spec = importlib.util.spec_from_file_location("m", "render.py"); sys.argv = [sys.argv[0], "x.png"]
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    res = check(ep, f"{name}.mp4", mod.TL)
    for n, ok, msg in res: print(("  ok  " if ok else "  FAIL"), n, "·", msg)
    print("rules", "PASS" if all(ok for _, ok, _ in res) else "FAIL")
