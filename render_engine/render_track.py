# render_track.py
# Full track renderer for SONICFRACZALATOR
# Rebuilds the legacy Fractal‑Chords pipeline in modular form

import numpy as np
import sys
import time

import params
from sonic_animation_engine.phase_shift import PhaseShift
from sonic_animation_engine.chaos_noise import ChaosNoise
from harmony_engine.chord_engine import ChordEngine
from voices.voice_engine import VoiceEngine
from render_engine.mixdown import Mixdown


def progress_bar(stage, i, total, bar_length=40):
    import shutil
    import os
    # Always initialize state if missing
    if not hasattr(progress_bar, "last_stage") or progress_bar.last_stage != stage:
        progress_bar.start_time = time.time()
        progress_bar.completions = []
        progress_bar.last_stage = stage
    if not hasattr(progress_bar, "completions"):
        progress_bar.completions = []
    if not hasattr(progress_bar, "start_time"):
        progress_bar.start_time = time.time()

    # Auto-detect terminal width and adjust bar length
    try:
        term_width = shutil.get_terminal_size((80, 20)).columns
    except Exception:
        term_width = 80
    reserved = len(" | | 100%  ETA 00:00") + len(stage)
    bar_length = max(10, min(30, term_width - reserved))

    frac = i / total
    filled = int(frac * bar_length)
    bar = "█" * filled + "-" * (bar_length - filled)
    percent = int(frac * 100)

    # Track completions for ETA
    now = time.time()
    if not progress_bar.completions or i > progress_bar.completions[-1][0]:
        progress_bar.completions.append((i, now))
        # Keep only the last 10 completions for smoothing
        if len(progress_bar.completions) > 10:
            progress_bar.completions = progress_bar.completions[-10:]

    # Estimate ETA based on average completion rate (chunks/sec), accounting for parallel workers
    if i == 0 or len(progress_bar.completions) < 2:
        eta_str = "--:--"
    else:
        # Calculate average completions per second
        completed_now, time_now = progress_bar.completions[-1]
        completed_then, time_then = progress_bar.completions[0]
        delta_chunks = completed_now - completed_then
        delta_time = time_now - time_then
        if delta_time > 0 and delta_chunks > 0:
            chunks_per_sec = delta_chunks / delta_time
            remaining_chunks = total - i
            # Estimate number of workers (processes) in use
            num_workers = os.cpu_count() or 4
            # Parallel ETA: remaining_chunks / (chunks_per_sec * num_workers)
            # But since we already see completions at the observed rate, just use chunks_per_sec
            remaining = remaining_chunks / chunks_per_sec
            if remaining < 1:
                eta_str = "--:--"
            else:
                eta_str = time.strftime("%M:%S", time.gmtime(remaining))
        else:
            eta_str = "--:--"

    sys.stdout.write(f"\r{stage} |{bar}| {percent:3d}%  ETA {eta_str}")
    sys.stdout.flush()

    if i == total:
        sys.stdout.write("\n")
        sys.stdout.flush()
        # Ensure next print starts on a new line
        print("")
        delattr(progress_bar, "start_time")
        if hasattr(progress_bar, "completions"):
            delattr(progress_bar, "completions")


def print_render_header(params):
    print("SONICFRACZALATOR — full track render starting...\n")
    print("=== CHAOS ENGINE ===")
    print(f"Attractor:        {params.ATTRACTOR}")
    print(f"Base dt:          {params.BASE_DT}")
    print(f"Chaos gearing:    {params.CHAOS_GEARING}")
    print(f"Effective dt:     {params.BASE_DT * params.CHAOS_GEARING:.6f}\n")
    print("=== TRACK SETTINGS ===")
    print(f"Track duration:   {params.TRACK_DUR_SECS} seconds")
    print(f"Chord duration:   {params.CHORD_DUR_SECS} seconds")
    print(f"Voices:           {params.VOICE_COUNT}")
    print(f"Sample rate:      {params.SAMPLE_RATE}\n")
    print("Render starting...\n")


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
            state = self.attractor.step()

            if isinstance(state, dict):
                x, y, z = state["x"], state["y"], state["z"]
            else:
                x, y, z = state[0], state[1], state[2]

            xs.append(x)
            ys.append(y)
            zs.append(z)

            if i % 1000 == 0:
                progress_bar("Attractor", i, num_steps - 1)

        # Ensure progress bar finishes and prints newline
        progress_bar("Attractor", num_steps - 1, num_steps - 1)
        print("")

        xs = np.array(xs)
        ys = np.array(ys)
        zs = np.array(zs)

        def norm(v):
            v = v - v.min()
            return v / (v.max() - v.min() + 1e-9)

        return norm(xs), norm(ys), norm(zs)

    # ----------------------------------------------------------
    # 2. Resample to audio rate
    # ----------------------------------------------------------
    def resample(self, X, Y, Z, num_samples):
        t_control = np.linspace(0, 1, len(X), endpoint=False)
        t_audio = np.linspace(0, 1, num_samples, endpoint=False)

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


        num_steps = int(
            params.TRACK_DUR_SECS *
            params.SAMPLE_RATE *
            params.BASE_DT *
            params.CHAOS_GEARING
        )

        X, Y, Z = self.generate_trajectory(num_steps)

        num_samples = int(params.TRACK_DUR_SECS * params.SAMPLE_RATE)
        Xi, Yi, Zi = self.resample(X, Y, Z, num_samples)

        print("3. Generating chaotic noise...")
        chaos = ChaosNoise(params)
        chaos_noise = chaos.generate(Xi, Yi, Zi)

        phase = PhaseShift(params.PHASE_SHIFT_MODE)

        harmony = ChordEngine(
            chord_sequence,
            params.CHORD_DUR_SECS,
            self.sample_rate
        )

        # Precompute per-voice base frequency lanes
        num_voices = harmony.num_voices
        base_freq_lanes = []
        for v in range(num_voices):
            freqs = np.zeros(num_samples, dtype=np.float32)
            for i in range(num_samples):
                freqs[i] = harmony.get_base_freq(i, v)
            base_freq_lanes.append(freqs)

        voices = VoiceEngine(self.sample_rate, params)

        print("\n4. Rendering voices...")


        # Calculate chunking for progress bar
        chunk_size = params.CHUNK_SIZE_SECONDS * params.SAMPLE_RATE
        num_chunks = int(np.ceil(num_samples / chunk_size))
        total_chunks = num_chunks * num_voices
        completed = 0

        def on_chunk_done(chunk_idx):
            nonlocal completed
            completed += 1
            progress_bar("Rendering chunks", completed, total_chunks)

        voice_signals = voices.render_voices(
            Xi, Yi, Zi,
            chaos_noise,
            base_freq_lanes,
            progress_callback=on_chunk_done
        )

        # Ensure progress bar is finalized and newline is printed
        progress_bar("Rendering chunks", total_chunks, total_chunks)
        print("")

        mixer = Mixdown(params)
        left, right = mixer.mix(voice_signals)

        print("5. Mixdown complete.")
        stereo = np.stack([left, right], axis=1).astype(np.float32)
        print("6. Track render finished.")
        print(f"Render complete, ready to write to:\n{self.output_path}")

        return stereo
