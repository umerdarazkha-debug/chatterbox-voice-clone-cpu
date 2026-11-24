# chatterbox-voice-clone-cpu

Clone a voice from a 30-second recording and make it read any text, on an Intel Mac with no graphics card.

It uses [Chatterbox](https://github.com/resemble-ai/chatterbox), the open-source text-to-speech model by Resemble AI (MIT). Chatterbox does not install on Intel Macs out of the box: the newest PyTorch has no Intel Mac builds, and some model files were saved on a GPU. This repo has the version pins and the one-line fix that make it work.

## What's in here

| File | What it does |
|---|---|
| `setup.sh` | Creates a Python 3.11 environment in `.venv` and installs Chatterbox with the pins below |
| `overrides.txt` | The version pins for Intel Macs, each one with the reason |
| `clone_voice.py` | Reads your text in the cloned voice and saves a `.wav` |
| `RECORDING.md` | How to record a voice sample that clones well, plus a paragraph to read |
| `examples/lines.txt` | A two-line test script |

## Setup

You need [uv](https://docs.astral.sh/uv/) and about 4 GB of free disk space.

```bash
git clone https://github.com/umerdarazkha-debug/chatterbox-voice-clone-cpu
cd chatterbox-voice-clone-cpu
./setup.sh
```

The first run downloads the model weights from Hugging Face (a few GB, about 10 minutes on a normal connection). After that it works offline.

## Use it

1. Record 20-40 seconds of the voice (see [RECORDING.md](RECORDING.md)) and save it as `my-voice.wav`.
2. Generate:

```bash
.venv/bin/python clone_voice.py --ref my-voice.wav --text "Hello, this is my cloned voice." -o hello.wav
```

A whole script, one line per chunk, each chunk also saved on its own:

```bash
.venv/bin/python clone_voice.py --ref my-voice.wav --text-file examples/lines.txt -o script.wav --lines-dir lines
```

Other languages use the multilingual model (23 languages; see the Chatterbox repo for the list). Only Hindi was tested here:

```bash
.venv/bin/python clone_voice.py --ref my-voice.wav --text "Hola, ¿qué tal?" --lang es -o hola.wav
```

### Settings

| Flag | Default | What it changes |
|---|---|---|
| `--exaggeration` | 0.5 | Emotion. 0.3-0.4 sounds calm, 0.7+ sounds hyped |
| `--cfg` | 0.5 | Pace. Lower (0.3) is slower and more deliberate |
| `--temperature` | 0.8 | Variation between takes |
| `--seed` | 7 | Same seed + same text = the same take. Change it to get a different one |
| `--pause` | 0.25 | Seconds of silence between lines |

Two combinations that work well: calm `--exaggeration 0.4 --cfg 0.5`, energetic `--exaggeration 0.7 --cfg 0.3`.

## How fast is it?

Slow, because it runs on the CPU. On a quad-core Intel MacBook Pro, loading the model takes under a minute and each sentence takes 1-2 minutes to generate. Write your script, start it, and do something else.

## The Intel Mac fixes

| Problem | Fix |
|---|---|
| PyTorch 2.3+ has no Intel Mac (x86_64) wheels | Pin `torch` and `torchaudio` to 2.2.2 |
| PyTorch 2.2.2 crashes with NumPy 2 | Pin `numpy<2` |
| Newer `numba`/`llvmlite` have no Intel Mac wheels for Python 3.11 | Pin `numba==0.60.0`, `llvmlite==0.43.0` |
| `ml_dtypes` version clash | Pin `ml_dtypes==0.5.1` |
| The Perth watermarker imports `pkg_resources`, removed in setuptools 81 | Pin `setuptools<81` |
| `pkuseg` fails to build in an isolated build environment | Install NumPy and Cython first, build `pkuseg` without isolation |
| A model file was saved on a CUDA GPU: `Attempting to deserialize object on a CUDA device` | `clone_voice.py` loads every tensor onto the CPU |

Tested with Python 3.11 and chatterbox-tts 0.1.4 on macOS 15 (Intel). It should also work on Apple Silicon and Linux, but there you can probably use the normal Chatterbox install.

## Use it responsibly

- Clone your own voice, or a voice you have clear permission to use. Don't use it to impersonate anyone.
- Every file Chatterbox makes carries an inaudible [Perth](https://github.com/resemble-ai/Perth) watermark, so the audio can be identified as AI-generated. This repo does not remove it.

## License

MIT for this repo. Chatterbox is MIT, by Resemble AI.
