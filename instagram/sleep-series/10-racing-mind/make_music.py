"""Calm ambient bed for the sleep-series reel — generated locally, no
samples, no licensing. Slow A-minor pad (A2/E3/A3/C4/E4) with detuned
sine partials, a slow breathing swell, sparse bell notes, soft noise
air, gentle low-pass and long fades. 27s to cover the 5-slide video."""
import numpy as np, wave

SR, DUR = 44100, 27.0
t = np.linspace(0, DUR, int(SR * DUR), endpoint=False)


def pad(freq, amp, detune=0.6, phase=0.0):
    v = np.zeros_like(t)
    for k, (mult, m_amp) in enumerate([(1, 1.0), (2, 0.22), (3, 0.09), (4, 0.04)]):
        for d in (-detune, 0.0, detune):
            v += m_amp * np.sin(2 * np.pi * (freq * mult + d) * t + phase + k)
    return amp * v / 9.0


def bell(freq, start, amp=0.16, decay=3.2):
    env = np.zeros_like(t)
    m = t >= start
    env[m] = np.exp(-(t[m] - start) / decay)
    tone = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2 * t)
    return amp * env * tone


# chord bed: A minor, add9 colour
sig = (pad(110.0, 0.55) + pad(164.81, 0.32) + pad(220.0, 0.30)
       + pad(261.63, 0.20, phase=1.1) + pad(329.63, 0.15, phase=2.2))

# slow breathing swell, ~9s cycle — the piece never sits still, never moves fast
sig *= 0.72 + 0.28 * (0.5 + 0.5 * np.sin(2 * np.pi * t / 9.0 - np.pi / 2))

# sparse bells land near the slide changes
for start, f in [(5.4, 440.0), (10.8, 523.25), (16.2, 329.63), (21.6, 440.0)]:
    sig += bell(f, start)

# a breath of filtered air under everything
rng = np.random.default_rng(7)
air = rng.normal(0, 1, t.size)
b = 0.0006
smooth = np.copy(air)
for _ in range(3):  # cheap repeated one-pole = very dark noise
    smooth = np.convolve(smooth, np.ones(400) / 400, mode="same")
sig += 0.05 * smooth / (np.abs(smooth).max() + 1e-9)

# gentle one-pole low-pass, warm not muffled
out = np.zeros_like(sig)
a = 0.055
prev = 0.0
for i in range(sig.size):
    prev += a * (sig[i] - prev)
    out[i] = prev

# long fade in / out so it can loop under the video without a seam
fi, fo = int(SR * 3.0), int(SR * 4.5)
env = np.ones_like(out)
env[:fi] = np.linspace(0, 1, fi) ** 2
env[-fo:] = np.linspace(1, 0, fo) ** 2
out *= env

out = out / (np.abs(out).max() + 1e-9) * 0.82
stereo = np.stack([out, np.roll(out, 300)], axis=1)  # slight width
pcm = (stereo * 32767).astype(np.int16)

with wave.open("audio/calm-bed.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("audio/calm-bed.wav", round(DUR, 1), "s")
