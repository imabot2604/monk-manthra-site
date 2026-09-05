"""
Reel 01 voiceover, Kokoro, rendered one line per file.

Per-line rather than one take on purpose: the script's line breaks are render
units, so a slow line can be given room on the timeline without re-rendering
everything. It also means a single garbled word costs one line, not the take.

Kokoro has no Indian English voice. bf_* are British, af_* American; for an
Indian brand the British voices sit closer to neutral, but this renders
candidates rather than deciding by assertion.
"""
import sys, numpy as np, soundfile as sf
from kokoro import KPipeline

LINES = [
    "A manthra is one word, repeated.",
    "Until it changes something.",
    "A body works the same way.",
    "One small dose, at the same hour.",
    "Golden Milk.",
    "Turmeric, ginger, cinnamon.",
    "And black pepper, because turmeric needs it.",
    "Monk Manthra. Coming soon.",
]

# The brand name is spelled "manthra" and must not be read that way. Kokoro
# turns that spelling into /mˈænθɹə/ - "man-THruh", with the English th of
# "think". The name comes from Sanskrit mantra, where the th is an aspirated
# t, so the correct sound is /mˈæntɹə/. Feeding the engine "mantra" produces
# exactly that. Verified by reading Kokoro's own phoneme output, not by ear.
#
# This only ever changes what the engine is told. Every visible spelling -
# captions, on-screen type, the post copy - stays "manthra".
SAY_AS = {"manthra": "mantra", "Manthra": "Mantra"}

SR = 24000
voice = sys.argv[1] if len(sys.argv) > 1 else "bf_emma"
# 0.85 rather than 1.0: the whole script is about not hurrying, and Kokoro's
# default read is brisk enough to undercut the words.
speed = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0

pipe = KPipeline(lang_code=voice[0], repo_id="hexgrad/Kokoro-82M")
parts, total = [], 0.0
for i, text in enumerate(LINES, 1):
    spoken = text
    for written, say in SAY_AS.items():
        spoken = spoken.replace(written, say)
    audio = np.concatenate([g.audio.numpy() for g in pipe(spoken, voice=voice, speed=speed)])
    sf.write(f"vo/{voice}-{i:02d}.wav", audio, SR)
    dur = len(audio) / SR
    total += dur
    parts.append(audio)
    print(f"  {i:02d}  {dur:5.2f}s  {text}")

# A single stitched preview, with the pauses the script asks for: the opening
# three lines only work with real silence between them.
gaps = [0.34, 0.46, 0.30, 0.46, 0.26, 0.16, 0.40, 0.0]
mix = []
for a, g in zip(parts, gaps):
    mix.append(a)
    mix.append(np.zeros(int(g * SR), dtype=a.dtype))
full = np.concatenate(mix)
sf.write(f"vo/{voice}-full.wav", full, SR)
print(f"\n{voice} @ {speed}  speech {total:.1f}s  with pauses {len(full)/SR:.1f}s")
