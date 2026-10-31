#!/bin/bash
# Re-render episodes (e.g. after a toolkit change) and push each to the media repo right away.
# usage: bash tools/rerender.sh 61 66 50 ...   → log: tools/rerender.log
K=$(cd "$(dirname "$0")/.." && pwd); M=/home/claude/notjustyou-media; LOG=$K/tools/rerender.log; : > $LOG
for n in "$@"; do
  nn=$(printf "%02d" $n); e=$(cd $K && ls -d ep${nn}_* | grep -v v3 | head -1)
  [ $n = 54 ] && e=ep54v3_lie_detector
  if (cd $K && python3 shared/build.py $e > /tmp/rr_$nn.txt 2>&1) && grep -q "verify PASS" /tmp/rr_$nn.txt; then
    cp $K/$e/$e.mp4 $K/publish/media/nj$nn.mp4 && cp $K/$e/$e.mp4 $M/nj$nn.mp4
    (cd $M && git add nj$nn.mp4 && git commit -qm "No. $nn: hard ending (no end card, no wipe)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KgYR2grBe2K1ok9D17dV8B" && (git push -q origin main || git push -q origin main)) >/dev/null 2>&1 \
      && echo "ok $nn $(grep -o '[0-9.]* s · verify' /tmp/rr_$nn.txt)" >> $LOG || echo "push-fail $nn" >> $LOG
  else echo "FAIL $nn $(tail -2 /tmp/rr_$nn.txt | tr '\n' ' ')" >> $LOG; fi
done
echo DONE >> $LOG
