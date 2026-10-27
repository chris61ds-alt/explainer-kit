"""Contact sheet at the end of every beat (+ frame 0):  python3 shared/sheet.py ep14_photo_memory [out.png]"""
import sys, os, subprocess, importlib.util
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ep = os.path.join(KIT, sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ep, "sheet.png")
os.chdir(ep)
spec = importlib.util.spec_from_file_location("r", "render.py"); argv = sys.argv; sys.argv = ["x", "x.png"]
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); sys.argv = argv
ts = [0.0] + [round(b["start"] + b["dur"] * .92, 2) for k, b in m.TL.T.items() if k != "end"] + [round(m.TL.S("end") + 1.2, 2)]
subprocess.run(["python3", "render.py", out, "--t", ",".join(map(str, ts))], check=True, capture_output=True)
print(out, ts)
