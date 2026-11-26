import json, csv, sys, glob, os
os.chdir("/home/claude/explainer-kit")
P = "publish/schedule.json"; rows = json.load(open(P)); have = {r[2] for r in rows[1:]}
for arg in sys.argv[1:]:
    n, date, time = arg.split(",")
    if n in have: continue
    e = glob.glob(f"ep{n}_*")[0]
    rows.append([date, time, n, e.split("_", 1)[1], f"nj{n}.mp4", f"nj{n}.jpg", open(f"{e}/caption.md").read().strip(), "", "", "", "", ""])
json.dump(rows, open(P, "w"), ensure_ascii=False, indent=0)
csv.writer(open("publish/schedule.csv", "w", newline="")).writerows(rows); print(len(rows) - 1, "rows")
