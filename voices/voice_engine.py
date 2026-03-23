# voice_engine.py
# Full per‑voice synthesis engine for SONICFRACZALATOR
# Ports the legacy Fractal‑Chords behaviour using modular components

import numpy as np
import time
import sys

from voices.oscillators import PhaseAccumulator, Oscillators
from voices.timbre import TimbreEngine
from voices.panning import PanningEngine
from sonic_animation_engine.micro_instability import MicroInstability
from sonic_animation_engine.groove_engine import GrooveEngine
from sonic_animation_engine.behaviour_engine import BehaviourEngine


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


class VoiceEngine:
    def __init__(self, sample_rate, params):
        self.sample_rate = sample_rate
        self.params = params
        self.micro = MicroInstability(params)
        self.groove = GrooveEngine(params)
        self.behaviour = BehaviourEngine(params)   # <-- Placeholder for future behaviour engine integration



        # Sub‑engines
        self.timbre_engine = TimbreEngine(depth=params.TIMBRE_DEPTH)
        self.panning_engine = PanningEngine(depth=params.PAN_DEPTH)

    def render_voice(
        self,
        Xi, Yi, Zi,
        chaos_noise,
        chord_engine,
        voice_index
    ):
        """
        Render a single voice buffer.
        Xi, Yi, Zi = chaotic lanes for this voice
        chaos_noise = chaotic noise field
        chord_engine = provides base frequencies
        """

        num_samples = len(Xi)
        left = np.zeros(num_samples, dtype=np.float32)
        right = np.zeros(num_samples, dtype=np.float32)

        phase = PhaseAccumulator(self.sample_rate)

        for i in range(num_samples):

            # --- 1. Base frequency from chord engine ---
            
            # --- Groove Emergence: timing offset ---
            if self.params.GROOVE_ON:
                groove_state = {"time_offset": 0.0}
                groove_state = self.groove.apply(groove_state, i / self.sample_rate)
                t_offset = groove_state["time_offset"]
            else:
                t_offset = 0.0
            # Apply timing offset to attractor lanes
            j = int(i + t_offset * self.sample_rate)

            # Clamp to valid range
            j = max(0, min(j, len(Xi) - 1))

            Xi_g = Xi[j]
            Yi_g = Yi[j]
            Zi_g = Zi[j]

            base_freq = chord_engine.get_base_freq(i, voice_index)

            # --- 2. Chaotic detune (legacy behaviour) ---
            cents = (Xi_g * 2 - 1) * self.params.DETUNE_CENTS


            if self.params.ENABLE_PITCH_NOISE:
                cents += (chaos_noise[i] * 2 - 1) * self.params.PITCH_NOISE_CENTS

            freq = base_freq * (2.0 ** (cents / 1200.0))
            # --- Micro-instability state (pitch excluded) ---
            voice_state = {
                "timbre": Yi[i],
                "amp": Zi[i],
                "pan_x": Xi[i],
                "pan_y": Yi[i],
            }

            # Apply micro-instability drift
            if self.params.MICRO_INSTABILITY_ON:
                voice_state = self.micro.apply(voice_state, i / self.sample_rate)
            # --- Behaviour Modulation ---
            behaviour_state = {
                "brightness": voice_state["timbre"],
                "amp_shape": voice_state["amp"],
                "chaos_depth": 0.0,
            }

            behaviour_state = self.behaviour.apply(
                behaviour_state,
                Yi_g,  # attractor lane after groove
                Zi_g
            )

            # Update voice_state with behaviour-modulated values
            voice_state["timbre"] = behaviour_state["brightness"]
            voice_state["amp"] = behaviour_state["amp_shape"]



            # --- 3. Oscillators ---
            p = phase.advance(freq)
            sine = Oscillators.sine(p)
            square = Oscillators.square(p)

            # --- 4. Timbre morphing ---
            if self.params.ENABLE_TIMBRE:
                sample = self.timbre_engine.apply(sine, square, voice_state["timbre"])    # <-- THIS LINE
            else:
                sample = sine

            # --- 5. Amplitude shaping ---
            if self.params.ENABLE_AMP:
                amp = Zi[i] ** self.params.AMP_EXPONENT
            else:
                amp = 1.0

            if self.params.ENABLE_AMP_NOISE:
                amp *= (1 + self.params.AMP_NOISE_DEPTH * (chaos_noise[i] - 0.5))

            sample *= amp

            # --- 6. Stereo panning ---
            if self.params.ENABLE_PAN:
                L, R = self.panning_engine.apply(sample, Xi_g, Yi_g)

            else:
                L = R = sample * 0.5

            left[i] = L
            right[i] = R

            if i % 5000 == 0:
                progress_bar(f"Voice {voice_index+1}", i, num_samples)

        return left, right

    def render_voices(
        self,
        Xi, Yi, Zi,
        chaos_noise,
        chord_engine
    ):
        """
        Render all voices and return a list of (left, right) arrays.
        """
        num_voices = chord_engine.num_voices
        voice_signals = []

        for v in range(num_voices):
            print(f"\n--- Voice {v+1}/{num_voices} ---")

            voice_start = time.time()

            left, right = self.render_voice(
                Xi, Yi, Zi,
                chaos_noise,
                chord_engine,
                voice_index=v
            )

            duration = time.time() - voice_start
            mins = int(duration // 60)
            secs = int(duration % 60)
            print()  # <-- forces newline after progress bar
            print(f"Voice {v+1} complete in {mins}m {secs}s")
 
            voice_signals.append((left, right))

        return voice_signals
