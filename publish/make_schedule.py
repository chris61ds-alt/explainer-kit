"""Erzeugt schedule.csv + schedule.json aus einer Reihenfolge.
python3 publish/make_schedule.py START_DATE "12:30,18:30" FIRST_SLOT_INDEX no1 no2 ...
FIRST_SLOT_INDEX: 0 = erster Slot des Starttags, 1 = zweiter usw."""
import csv, json, glob, os, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
start, times, first = sys.argv[1], sys.argv[2].split(","), int(sys.argv[3]); order = [int(x) for x in sys.argv[4:]]
HEAD = ["date","time","no","title","video_file","cover_file","caption","ig_status","ig_container","ig_media_id","ig_posted_at","tiktok_done"]
d = dt.date.fromisoformat(start); slot = first; rows = []
for n in order:
    e = [p for p in glob.glob(os.path.join(ROOT, f"ep{n:02d}_*")) if os.path.isdir(p)][0]
    for ext in ("mp4", "jpg"):
        assert os.path.exists(os.path.join(HERE, "media", f"nj{n:02d}.{ext}")), f"media fehlt: nj{n:02d}.{ext}"
    rows.append([str(d), times[slot], str(n), os.path.basename(e).split("_", 1)[1], f"nj{n:02d}.mp4", f"nj{n:02d}.jpg",
                 open(os.path.join(e, "caption.md")).read().strip(), "", "", "", "", ""])
    slot += 1
    if slot >= len(times): slot = 0; d += dt.timedelta(days=1)
assert len(set(order)) == len(order), "doppelte Folge"
w = csv.writer(open(os.path.join(HERE, "schedule.csv"), "w", newline="")); w.writerow(HEAD); w.writerows(rows)
json.dump([HEAD] + rows, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False, indent=0)
print(len(rows), "Folgen", rows[0][0], rows[0][1], "→", rows[-1][0], rows[-1][1])
