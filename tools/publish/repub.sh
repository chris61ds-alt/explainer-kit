#!/bin/bash
# repub.sh epNNN_name -> replace media of an already scheduled episode (rules must PASS)
K="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M="${NJY_MEDIA:-$(cd "$K/.." && pwd)/notjustyou-media}"   # paths from the script location (26.11.2026)
e=$1; n=$(echo $e | sed -E 's/^ep0*([0-9]+)_.*/\1/'); cd $K
grep -q '"rules": "PASS"' $e/build_report.json || { echo "rules FAIL - not published"; exit 1; }
cp $e/$e.mp4 $M/nj$n.mp4 && python3 -c "from PIL import Image; Image.open('$e/${e}_cover.png').convert('RGB').save('$M/nj$n.jpg', quality=90)"
rm -f tools/checklist/thumbs/nj$n.jpg; (cd tools/checklist && python3 make_eps.py >/dev/null && python3 build.py >/dev/null)
git add -A $e shared tools/checklist && git commit -qm "No. $n remake (REGELN.md: hook, first 3 s, payoff camera, rules PASS)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KgYR2grBe2K1ok9D17dV8B" && git push -q
cd $M && git add nj$n.mp4 nj$n.jpg && git commit -qm "nj$n remake

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KgYR2grBe2K1ok9D17dV8B" && git push -q && echo "republished nj$n"
