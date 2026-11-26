#!/bin/bash
# pub.sh epNNN_name date time  -> media + schedule + checklist + commits/push
K="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M="${NJY_MEDIA:-$(cd "$K/.." && pwd)/notjustyou-media}"   # paths from the script location (26.11.2026)
e=$1; n=$(echo $e | sed -E 's/^ep0*([0-9]+)_.*/\1/'); cd $K
grep -q '"rules": "PASS"' $e/build_report.json || { echo "rules FAIL - not published"; exit 1; }
cp $e/$e.mp4 $M/nj$n.mp4 && python3 -c "from PIL import Image; Image.open('$e/${e}_cover.png').convert('RGB').save('$M/nj$n.jpg', quality=90)"
python3 "$K/tools/publish/sched.py" $n,$2,$3 && cp publish/schedule.json $M/
rm -f tools/checklist/thumbs/nj$n.jpg; (cd tools/checklist && python3 make_eps.py && python3 build.py | tail -1)
git add -A $e shared publish/schedule.* tools/checklist PROJEKT.md && git commit -qm "No. $n $e

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KgYR2grBe2K1ok9D17dV8B" && git push -q
cd $M && git add nj$n.mp4 nj$n.jpg schedule.json && git commit -qm "nj$n + schedule

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KgYR2grBe2K1ok9D17dV8B" && git push -q && echo "published nj$n"
