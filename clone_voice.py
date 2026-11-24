"""Speak any text in a cloned voice with Chatterbox, on a CPU (built for Intel Macs).

Examples:
  .venv/bin/python clone_voice.py --ref my-voice.wav --text "Hello there" -o hello.wav
  .venv/bin/python clone_voice.py --ref my-voice.wav --text-file examples/lines.txt -o script.wav
  .venv/bin/python clone_voice.py --ref my-voice.wav --text "Hola" --lang es -o hola.wav

--text-file: one line = one chunk. Chunks are joined with a short pause, and
--lines-dir also saves each chunk as its own file (line00.wav, line01.wav ...).

Tone:  --exaggeration 0.3 calm .. 0.5 default .. 0.8 hyped
Pace:  --cfg 0.3 slower and more deliberate .. 0.5 default
"""
import argparse
import os
import sys
import time

p = argparse.ArgumentParser(description="Clone a voice from a short sample and speak your text with it.")
p.add_argument("--ref", required=True, help="5-30 s clean recording of the voice to clone (.wav, .mp3, .m4a)")
src = p.add_mutually_exclusive_group(required=True)
src.add_argument("--text", help="the text to speak")
src.add_argument("--text-file", help="a text file, one chunk per line")
p.add_argument("-o", "--out", required=True, help="output .wav file")
p.add_argument("--exaggeration", type=float, default=0.5, help="emotion, 0.25-1.0 (default 0.5)")
p.add_argument("--cfg", type=float, default=0.5, help="pace/guidance, 0.2-0.7 (default 0.5)")
p.add_argument("--temperature", type=float, default=0.8)
p.add_argument("--seed", type=int, default=7, help="same seed + same text = same take")
p.add_argument("--pause", type=float, default=0.25, help="seconds of silence between lines")
p.add_argument("--lang", help="language code for the multilingual model, e.g. es, fr, de, hi")
p.add_argument("--lines-dir", help="also save every line as its own file in this folder")
a = p.parse_args()

if not os.path.isfile(a.ref):
    sys.exit(f"Voice sample not found: {a.ref}")
if a.text:
    lines = [a.text.strip()]
else:
    if not os.path.isfile(a.text_file):
        sys.exit(f"Text file not found: {a.text_file}")
    with open(a.text_file, encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
if not any(lines):
    sys.exit("Nothing to say: the text is empty.")
if a.lines_dir:
    os.makedirs(a.lines_dir, exist_ok=True)

import torch  # noqa: E402  (imported after argument checks so --help is instant)
import torchaudio as ta  # noqa: E402

# Some checkpoints on the Hugging Face hub were saved on a CUDA GPU.
# Load every tensor onto the CPU instead, so a Mac without CUDA can open them.
_load = torch.load
torch.load = lambda *args, **kw: _load(*args, **{**kw, "map_location": kw.get("map_location") or "cpu"})

torch.manual_seed(a.seed)
t0 = time.time()
extra = {}
if a.lang:
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    extra["language_id"] = a.lang
else:
    from chatterbox.tts import ChatterboxTTS
    model = ChatterboxTTS.from_pretrained(device="cpu")
print(f"model loaded in {time.time() - t0:.0f} s")

gap = torch.zeros(1, int(model.sr * a.pause))
chunks = []
for i, line in enumerate(lines):
    t1 = time.time()
    print(f"[{i + 1}/{len(lines)}] {line[:70]}")
    wav = model.generate(
        line,
        audio_prompt_path=a.ref,
        exaggeration=a.exaggeration,
        cfg_weight=a.cfg,
        temperature=a.temperature,
        **extra,
    )
    print(f"    {wav.shape[1] / model.sr:.1f} s of audio in {time.time() - t1:.0f} s")
    chunks += [wav, gap]
    if a.lines_dir:
        ta.save(os.path.join(a.lines_dir, f"line{i:02d}.wav"), wav, model.sr)

ta.save(a.out, torch.cat(chunks[:-1], dim=1), model.sr)
print("saved", a.out)
