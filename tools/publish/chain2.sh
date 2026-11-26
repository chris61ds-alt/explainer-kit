#!/bin/bash
cd /home/claude/explainer-kit
while pgrep -f "shared/build.py" >/dev/null; do sleep 4; done
for e in "$@"; do
  python3 shared/build.py $e > /tmp/b_$e.log 2>&1
  grep -A30 "^== " /tmp/b_$e.log | grep -v "voice:" >> /tmp/q.log
done
echo DONE >> /tmp/q.log
