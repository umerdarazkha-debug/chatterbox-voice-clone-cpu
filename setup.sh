#!/bin/sh
# Creates a Python 3.11 environment with Chatterbox in ./.venv
# Needs uv: https://docs.astral.sh/uv/  (curl -LsSf https://astral.sh/uv/install.sh | sh)
set -e
cd "$(dirname "$0")"
command -v uv >/dev/null 2>&1 || { echo "uv not found. Install it first: https://docs.astral.sh/uv/"; exit 1; }
uv venv --clear --python 3.11 .venv
# pkuseg (a dependency) needs numpy and cython present while it builds
uv pip install --python .venv/bin/python "numpy<2" "setuptools<81" cython wheel
uv pip install --python .venv/bin/python --override overrides.txt \
  --no-build-isolation-package pkuseg "chatterbox-tts==0.1.4"
echo
echo "Done. Try it:"
echo "  .venv/bin/python clone_voice.py --ref my-voice.wav --text \"Hello, this is my cloned voice.\" -o hello.wav"
