# render_track.py
# Full track renderer for SONICFRACZALATOR
# Rebuilds the legacy Fractal‑Chords pipeline in modular form

import numpy as np
import time
import sys

from sonic_animation_engine.phase_shift import PhaseShift
from sonic_animation_engine.chaos_noise import ChaosNoise
from harmony_engine.chord_engine import ChordEngine
from voices.voice_engine import VoiceEngine
from render_engine.mixdown import Mixdown


def progress_bar(stage, i, total, bar_length=30):
    frac = i / total
    filled = int(frac * bar_length)
    bar = "█" * filled + "-" * (bar_length - filled)

    now = time.time()
    if i == 0:
        progress_bar.start_time = now
        eta_str = "--:--"
    else:
        elapsed = now - progress_bar.start_time
        remaining = elapsed * (total - i) / i
        eta_str = time.strftime("%M:%S", time.gmtime(remaining))

    sys.stdout.write(f"\r{stage} |{bar}| {int(frac*100):3d}%  ETA {eta_str}")
    sys.stdout.flush()

    if i == total - 1:
        sys.stdout.write("\n")
        sys.stdout.flush()


class TrackRenderer:
    def __init__(self, params, attractor):
        self.params = params
        self.attractor = attractor
        self.sample_rate = params.SAMPLE_RATE
        self.output_path = params.WAV_OUTPUT_PATH

    # ----------------------------------------------------------
    # 1. Generate attractor trajectory
    # ----------------------------------------------------------
    def generate_trajectory(self, num_steps):
        xs, ys, zs = [], [], []

        x = 0.8
        y = 0.02
        z = 0.5
        print("1. Generating attractor trajectory...")

        for i in range(num_steps):
            state = self.attractor.step()
            x, y, z = state["x"], state["y"], state["z"]
            xs.append(x)
            ys.append(y)
            zs.append(z)

            if i % 1000 == 0:
                progress_bar("Attractor", i, num_steps)

        xs = np.array(xs)
        ys = np.array(ys)
        zs = np.array(zs)

        # Normalise like legacy
        def norm(v):
            v = v - v.min()
            return v / (v.max() - v.min() + 1e-9)

        return norm(xs), norm(ys), norm(zs)

    # ----------------------------------------------------------
    # 2. Resample to audio rate
    # ----------------------------------------------------------
    def resample(self, X, Y, Z, num_samples):
        t_control = np.linspace(0, 1, len(X), endpoint=False)
        t_audio   = np.linspace(0, 1, num_samples, endpoint=False)

        print("2. Resampling to audio rate...")

        Xi = np.interp(t_audio, t_control, X)
        Yi = np.interp(t_audio, t_control, Y)
        Zi = np.interp(t_audio, t_control, Z)

        return Xi, Yi, Zi

    # ----------------------------------------------------------
    # 3. Full track render
    # ----------------------------------------------------------
    def render(self, chord_sequence):
        params = self.params

        # Number of attractor steps
        num_steps = int(
            params.TRACK_DUR_SECS *
            params.SAMPLE_RATE *
            params.BASE_DT *
            params.CHAOS_GEARING
        )

        # 1. Attractor trajectory
        X, Y, Z = self.generate_trajectory(num_steps)

        # 2. Resample to audio rate
        num_samples = int(params.TRACK_DUR_SECS * params.SAMPLE_RATE)
        Xi, Yi, Zi = self.resample(X, Y, Z, num_samples)

        # 3. Chaotic noise + engines
        print("3. Generating chaotic noise...")
        chaos = ChaosNoise(params)

        # PhaseShift is available for future per‑voice lanes if you wire it in
        phase = PhaseShift(params.PHASE_SHIFT_MODE)

        harmony = ChordEngine(
            chord_sequence,
            params.CHORD_DUR_SECS,
            self.sample_rate
        )

        voices = VoiceEngine(self.sample_rate, params)

        print("4. Rendering voices...")
        voice_signals = voices.render_voices(
            Xi, Yi, Zi,
            chaos_noise=chaos.generate(Xi, Yi, Zi),
            chord_engine=harmony
        )

        # 4. Mixdown
        mixer = Mixdown(params)
        left, right = mixer.mix(voice_signals)

        print("5. Mixdown complete.")
        stereo = np.stack([left, right], axis=1).astype(np.float32)
        print("6. Track render finished.")
        print(f"Render complete, ready to write to:\n{self.output_path}")
        return stereo
