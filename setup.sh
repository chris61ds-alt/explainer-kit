#!/usr/bin/env bash
# Einmal pro neuer Umgebung:  bash setup.sh
# Installiert alles, was die Produktion braucht (idempotent – mehrfach ausführen schadet nicht).
set -e
cd "$(dirname "$0")"
echo "1/4 Python-Pakete"
pip install -q kokoro-onnx==0.6.1 sherpa-onnx soundfile scipy numpy pillow --break-system-packages 2>/dev/null \
  || pip install -q kokoro-onnx==0.6.1 sherpa-onnx soundfile scipy numpy pillow
echo "2/4 ffmpeg"
command -v ffmpeg >/dev/null || { (apt-get update -qq && apt-get install -y -qq ffmpeg) || { echo "ffmpeg fehlt und konnte nicht installiert werden"; exit 1; }; }
echo "3/4 Stimme (Kokoro, ~340 MB)"
mkdir -p ~/kokoro
[ -s ~/kokoro/kokoro-v1.0.onnx ] || curl -sSL -o ~/kokoro/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -s ~/kokoro/voices-v1.0.bin ]  || curl -sSL -o ~/kokoro/voices-v1.0.bin  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
echo "4/4 Spracherkennung (Whisper base.en, ~200 MB)"
mkdir -p ~/asr
[ -d ~/asr/sherpa-onnx-whisper-base.en ] || (cd ~/asr && curl -sSL -o w.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.en.tar.bz2 && tar xjf w.tar.bz2 && rm w.tar.bz2)
python3 - <<'PY'
import os, kokoro_onnx, sherpa_onnx, soundfile, scipy, PIL
for p in ["~/kokoro/kokoro-v1.0.onnx", "~/kokoro/voices-v1.0.bin", "~/asr/sherpa-onnx-whisper-base.en/base.en-encoder.int8.onnx", "fonts/Roboto-Black.woff"]:
    assert os.path.exists(os.path.expanduser(p)), "fehlt: " + p
print("Setup OK – Test: python3 shared/build.py ep77_casual")
PY
