#!/bin/bash
# repub.sh epNNN_name -> replace media of an already scheduled episode (rules must PASS)
K="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M="${NJY_MEDIA:-$(cd "$K/.." && pwd)/notjustyou-media}"   # paths from the script location (26.11.2026)
e=$1; n=$(echo $e | sed -E 's/^ep0*([0-9]+)[a-z]?_.*/\1/'); cd $K
grep -q '"rules": "PASS"' $e/build_report.json || { echo "rules FAIL - not published"; exit 1; }
cp $e/$e.mp4 $M/nj$n.mp4 && python3 -c "from PIL import Image; Image.open('$e/${e}_cover.png').convert('RGB').save('$M/nj$n.jpg', quality=90)"
python3 - "$n" <<'PY'                 # 27.11.2026: a remake also replaces the caption in the schedule
import json, csv, glob, sys
n = sys.argv[1]; P = "publish/schedule.json"; rows = json.load(open(P)); e = glob.glob(f"ep{n}_*")[0]
for r in rows[1:]:
    if r[2] == n: r[6] = open(f"{e}/caption.md").read().strip()
json.dump(rows, open(P, "w"), ensure_ascii=False, indent=0); csv.writer(open("publish/schedule.csv", "w", newline="")).writerows(rows)
PY
cp publish/schedule.json $M/
rm -f tools/checklist/thumbs/nj$n.jpg; (cd tools/checklist && python3 make_eps.py >/dev/null && python3 build.py >/dev/null)
git add -A $e shared tools/checklist publish/schedule.* && git commit -qm "No. $n remake (REGELN.md: hook, first 3 s, payoff camera, rules PASS)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
${NJY_SESSION:+Claude-Session: $NJY_SESSION}" && git push -q
cd $M && git add nj$n.mp4 nj$n.jpg schedule.json && git commit -qm "nj$n remake

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
${NJY_SESSION:+Claude-Session: $NJY_SESSION}" && git push -q && echo "republished nj$n"
