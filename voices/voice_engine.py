# voice_engine.py
# Full per‑voice synthesis engine for SONICFRACZALATOR

import numpy as np

from voices.oscillators import PhaseAccumulator, Oscillators
from voices.timbre import TimbreEngine
from voices.panning import PanningEngine
from sonic_animation_engine.micro_instability import MicroInstability
from sonic_animation_engine.groove_engine import GrooveEngine

# voice_engine.py
# Full per‑voice synthesis engine for SONICFRACZALATOR

import numpy as np
from voices.oscillators import PhaseAccumulator, Oscillators
from voices.timbre import TimbreEngine
from voices.panning import PanningEngine
from sonic_animation_engine.micro_instability import MicroInstability
from sonic_animation_engine.groove_engine import GrooveEngine
from sonic_animation_engine.behaviour_engine import BehaviourEngine

class VoiceEngine:
    def __init__(self, sample_rate, params):
        self.sample_rate = sample_rate
        self.params = params
        self.micro = MicroInstability(params)
        self.groove = GrooveEngine(params)
        self.behaviour = BehaviourEngine(params)
        self.timbre_engine = TimbreEngine(depth=params.TIMBRE_DEPTH)
        self.panning_engine = PanningEngine(depth=params.PAN_DEPTH)

    def render_voice(self, Xi, Yi, Zi, chaos_noise, base_freq_lane, voice_index):
        num_samples = len(Xi)
        left = np.zeros(num_samples, dtype=np.float32)
        right = np.zeros(num_samples, dtype=np.float32)
        phase = PhaseAccumulator(self.sample_rate)
        for i in range(num_samples):
            if self.params.GROOVE_ON:
                groove_state = {"time_offset": 0.0}
                groove_state = self.groove.apply(groove_state, i / self.sample_rate)
                t_offset = groove_state["time_offset"]
            else:
                t_offset = 0.0
            j = int(i + t_offset * self.sample_rate)
            j = max(0, min(j, len(Xi) - 1))
            Xi_g = Xi[j]
            Yi_g = Yi[j]
            Zi_g = Zi[j]
            base_freq = base_freq_lane[i]
            cents = (Xi_g * 2 - 1) * self.params.DETUNE_CENTS
            if self.params.ENABLE_PITCH_NOISE:
                cents += (chaos_noise[i] * 2 - 1) * self.params.PITCH_NOISE_CENTS
            freq = base_freq * (2.0 ** (cents / 1200.0))
            voice_state = {
                "timbre": Yi[i],
                "amp": Zi[i],
                "pan_x": Xi[i],
                "pan_y": Yi[i],
            }
            if self.params.MICRO_INSTABILITY_ON:
                voice_state = self.micro.apply(voice_state, i / self.sample_rate)
            behaviour_state = {
                "brightness": voice_state["timbre"],
                "amp_shape": voice_state["amp"],
                "chaos_depth": 0.0,
            }
            behaviour_state = self.behaviour.apply(
                behaviour_state,
                Yi_g,
                Zi_g
            )
            voice_state["timbre"] = behaviour_state["brightness"]
            voice_state["amp"] = behaviour_state["amp_shape"]
            p = phase.advance(freq)
            sine = Oscillators.sine(p)
            square = Oscillators.square(p)
            if self.params.ENABLE_TIMBRE:
                sample = self.timbre_engine.apply(sine, square, voice_state["timbre"])
            else:
                sample = sine
            if self.params.ENABLE_AMP:
                amp = Zi[i] ** self.params.AMP_EXPONENT
            else:
                amp = 1.0
            if self.params.ENABLE_AMP_NOISE:
                amp *= (1 + self.params.AMP_NOISE_DEPTH * (chaos_noise[i] - 0.5))
            sample *= amp
            if self.params.ENABLE_PAN:
                L, R = self.panning_engine.apply(sample, Xi_g, Yi_g)
            else:
                L = R = sample * 0.5
            left[i] = L
            right[i] = R
        return left, right

    def render_voice_chunk(self, Xi, Yi, Zi, chaos_noise, base_freq_lane, voice_index, start, end):
        Xi_chunk = Xi[start:end]
        Yi_chunk = Yi[start:end]
        Zi_chunk = Zi[start:end]
        chaos_noise_chunk = chaos_noise[start:end]
        base_freq_lane_chunk = base_freq_lane[start:end]
        left, right = self.render_voice(
            Xi_chunk, Yi_chunk, Zi_chunk,
            chaos_noise_chunk,
            base_freq_lane_chunk,
            voice_index
        )
        return (voice_index, start, end, left, right)

    def render_voices_chunked(self, Xi, Yi, Zi, chaos_noise, base_freq_lanes, progress_callback=None):
        import concurrent.futures
        import math
        import os
        num_voices = len(base_freq_lanes)
        num_samples = len(Xi)
        # Set chunk size to 1 second for regular updates
        chunk_size = int(1 * self.sample_rate)
        num_chunks = math.ceil(num_samples / chunk_size)
        voice_signals = [
            (np.zeros(num_samples, dtype=np.float32), np.zeros(num_samples, dtype=np.float32))
            for _ in range(num_voices)
        ]
        params_dict = {k: v for k, v in self.params.__dict__.items() if not k.startswith('__') and not callable(v)}
        sample_rate = self.sample_rate

        def chunk_args():
            for c in range(num_chunks):
                start = c * chunk_size
                end = min((c + 1) * chunk_size, num_samples)
                Xi_chunk = Xi[start:end]
                Yi_chunk = Yi[start:end]
                Zi_chunk = Zi[start:end]
                chaos_noise_chunk = chaos_noise[start:end]
                base_freq_lanes_chunk = [lane[start:end] for lane in base_freq_lanes]
                yield (Xi_chunk, Yi_chunk, Zi_chunk, chaos_noise_chunk, base_freq_lanes_chunk, params_dict, sample_rate, start, end)

        max_workers = os.cpu_count() or 4
        args_iter = iter(chunk_args())
        futures = []
        completed = 0

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Prime the pool with up to max_workers jobs
            for _ in range(max_workers):
                try:
                    args = next(args_iter)
                    futures.append(executor.submit(render_time_chunk_all_voices_stateless, *args))
                except StopIteration:
                    break

            while futures:
                done, not_done = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
                futures = list(not_done)
                for fut in done:
                    start, end, lefts, rights = fut.result()
                    for v in range(num_voices):
                        voice_signals[v][0][start:end] = lefts[v]
                        voice_signals[v][1][start:end] = rights[v]
                    completed += 1
                    if progress_callback:
                        progress_callback(completed)
                    # Submit the next chunk, if any
                    try:
                        args = next(args_iter)
                        futures.append(executor.submit(render_time_chunk_all_voices_stateless, *args))
                    except StopIteration:
                        pass
        return voice_signals

    def render_voices(self, Xi, Yi, Zi, chaos_noise, base_freq_lanes, progress_callback=None):
        return self.render_voices_chunked(
            Xi, Yi, Zi,
            chaos_noise,
            base_freq_lanes,
            progress_callback=progress_callback
        )


# Stateless chunk worker for multiprocessing: processes all voices for a time chunk
def render_time_chunk_all_voices_stateless(
    Xi_chunk, Yi_chunk, Zi_chunk, chaos_noise_chunk, base_freq_lanes_chunk, params_dict, sample_rate, start, end
):
    import numpy as np
    import sys
    from voices.oscillators import PhaseAccumulator, Oscillators
    from voices.timbre import TimbreEngine
    from voices.panning import PanningEngine
    from sonic_animation_engine.micro_instability import MicroInstability
    from sonic_animation_engine.groove_engine import GrooveEngine
    from sonic_animation_engine.behaviour_engine import BehaviourEngine
    # Suppress all print statements in worker processes
    class DummyFile:
        def write(self, x): pass
        def flush(self): pass
    sys.stdout = DummyFile()
    sys.stderr = DummyFile()
    class P:
        pass
    p = P()
    for k, v in params_dict.items():
        setattr(p, k, v)
    num_voices = len(base_freq_lanes_chunk)
    num_samples = len(Xi_chunk)
    lefts = []
    rights = []
    for v in range(num_voices):
        micro = MicroInstability(p)
        groove = GrooveEngine(p)
        behaviour = BehaviourEngine(p)
        timbre_engine = TimbreEngine(depth=p.TIMBRE_DEPTH)
        panning_engine = PanningEngine(depth=p.PAN_DEPTH)
        phase = PhaseAccumulator(sample_rate)
        left = np.zeros(num_samples, dtype=np.float32)
        right = np.zeros(num_samples, dtype=np.float32)
        for i in range(num_samples):
            if p.GROOVE_ON:
                groove_state = {"time_offset": 0.0}
                groove_state = groove.apply(groove_state, i / sample_rate)
                t_offset = groove_state["time_offset"]
            else:
                t_offset = 0.0
            j = int(i + t_offset * sample_rate)
            j = max(0, min(j, num_samples - 1))
            Xi_g = Xi_chunk[j]
            Yi_g = Yi_chunk[j]
            Zi_g = Zi_chunk[j]
            base_freq = base_freq_lanes_chunk[v][i]
            cents = (Xi_g * 2 - 1) * p.DETUNE_CENTS
            if p.ENABLE_PITCH_NOISE:
                cents += (chaos_noise_chunk[i] * 2 - 1) * p.PITCH_NOISE_CENTS
            freq = base_freq * (2.0 ** (cents / 1200.0))
            voice_state = {
                "timbre": Yi_chunk[i],
                "amp": Zi_chunk[i],
                "pan_x": Xi_chunk[i],
                "pan_y": Yi_chunk[i],
            }
            if p.MICRO_INSTABILITY_ON:
                voice_state = micro.apply(voice_state, i / sample_rate)
            behaviour_state = {
                "brightness": voice_state["timbre"],
                "amp_shape": voice_state["amp"],
                "chaos_depth": 0.0,
            }
            behaviour_state = behaviour.apply(
                behaviour_state,
                Yi_g,
                Zi_g
            )
            voice_state["timbre"] = behaviour_state["brightness"]
            voice_state["amp"] = behaviour_state["amp_shape"]
            pval = phase.advance(freq)
            sine = Oscillators.sine(pval)
            square = Oscillators.square(pval)
            if p.ENABLE_TIMBRE:
                sample = timbre_engine.apply(sine, square, voice_state["timbre"])
            else:
                sample = sine
            if p.ENABLE_AMP:
                amp = Zi_chunk[i] ** p.AMP_EXPONENT
            else:
                amp = 1.0
            if p.ENABLE_AMP_NOISE:
                amp *= (1 + p.AMP_NOISE_DEPTH * (chaos_noise_chunk[i] - 0.5))
            sample *= amp
            if p.ENABLE_PAN:
                L, R = panning_engine.apply(sample, Xi_g, Yi_g)
            else:
                L = R = sample * 0.5
            left[i] = L
            right[i] = R
        lefts.append(left)
        rights.append(right)
    return (start, end, lefts, rights)
