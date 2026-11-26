import sys, os, importlib.util
ep = os.path.abspath(sys.argv[1]); sys.path.insert(0, os.path.join(ep, "..", "shared")); os.chdir(ep)
spec = importlib.util.spec_from_file_location("m", "render.py"); sys.argv = ["x", "x.png"]
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(round(m.TL.total, 2), {k: round(v["start"], 2) for k, v in m.TL.T.items()})
