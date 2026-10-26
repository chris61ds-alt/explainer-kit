"""Gate the final encoded MP4 (its actual bytes)."""
import subprocess, json, sys, re, hashlib, os
f = sys.argv[1]; res = {}; ok = True
def run(c): return subprocess.run(c, capture_output=True, text=True)
pr = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", f]).stdout)
v = [s for s in pr["streams"] if s["codec_type"] == "video"][0]; a = [s for s in pr["streams"] if s["codec_type"] == "audio"][0]
res["video"] = f'{v["codec_name"]} {v["width"]}x{v["height"]} {v["pix_fmt"]} {v["r_frame_rate"]}'
res["audio"] = f'{a["codec_name"]} {a["sample_rate"]} Hz {a["channels"]}ch'
res["duration_s"] = round(float(pr["format"]["duration"]), 2)
res["size_MiB"] = round(os.path.getsize(f) / 2**20, 1)
checks = {"spec": v["codec_name"] == "h264" and v["width"] == 1080 and v["height"] == 1920 and v["pix_fmt"] == "yuv420p" and v["r_frame_rate"] == "30/1" and a["codec_name"] == "aac",
          "size<=95MiB": res["size_MiB"] <= 95}
bd = run(["ffmpeg", "-i", f, "-vf", "blackdetect=d=0.5:pix_th=0.04", "-an", "-f", "null", "-"]).stderr
res["black_intervals"] = re.findall(r"black_start:[\d.]+ black_end:[\d.]+", bd); checks["no_black"] = not res["black_intervals"]
eb = run(["ffmpeg", "-i", f, "-af", "ebur128=peak=true", "-vn", "-f", "null", "-"]).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)[-1]); TP = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", eb)[-1])
res["loudness_LUFS"] = I; res["true_peak_dBTP"] = TP
checks["loudness -18..-14"] = -18 <= I <= -14; checks["true_peak<=-1"] = TP <= -1.0
res["sha256"] = hashlib.sha256(open(f, "rb").read()).hexdigest()
res["checks"] = checks
print(json.dumps(res, indent=1)); print("PASS" if all(checks.values()) else "FAIL")
