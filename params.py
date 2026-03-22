# params.py
# Global parameter definitions for SONICFRACZALATOR

class VibeParams:
    def __init__(self):
        # -----------------------------
        # ATTRACTOR SELECTION
        # -----------------------------
        self.ATTRACTOR = "rossler"   # or "lorenz", "halvorsen", etc.
        self.BASE_DT = 0.01          # base integration timestep
        self.CHAOS_GEARING = 1.0     # multiplier for chaos speed

        # -----------------------------
        # AUDIO ENGINE
        # -----------------------------
        self.SAMPLE_RATE = 44100     # Hz
        self.TRACK_DUR_SECS = 10     # seconds

        # -----------------------------
        # OUTPUT PATH
        # -----------------------------
        self.WAV_OUTPUT_PATH = r"C:\Temp\fancychord.wav"

        # -----------------------------
        # PHASE SHIFT (per‑voice chaos lanes)
        # -----------------------------
        self.PHASE_SHIFT_MODE = "even"   # options: "even", "random", "golden_ratio"

        # -----------------------------
        # HARMONY ENGINE — from original Fractal-Chords.py
        # -----------------------------
        self.CHORD_SEQUENCE = [
            [82.41, 110.00, 138.59, 146.83, 220.00],
            [55.00, 110.00, 138.59, 164.81, 277.18],
            [55.00, 110.00, 130.81, 164.81, 261.63],
            [49.00, 98.00, 130.81, 146.83, 261.63],
            [49.00, 98.00, 123.47, 146.83, 246.94],
        ]

        # Duration of each chord segment (seconds)
        # Matches legacy Fractal‑Chords default of 6.0 seconds
        self.CHORD_DUR_SECS = 6.0

        # -----------------------------
        # TIMBRE ENGINE (sine → square morphing)
        # -----------------------------
        self.ENABLE_TIMBRE = True
        self.TIMBRE_DEPTH = 1.0      # 0 = pure sine, 1 = full morph

        # -----------------------------
        # PANNING ENGINE
        # -----------------------------
        self.ENABLE_PAN = True
        self.PAN_DEPTH = 1.0         # 0 = mono, 1 = full stereo spread

        # -----------------------------
        # LEGACY FRACTAL‑CHORDS SYNTH CONTROLS
        # (required by VoiceEngine, ChaosNoise, Mixdown)
        # -----------------------------

        # Pitch modulation
        self.DETUNE_CENTS = 40.0            # Max chaotic detune in cents
        self.ENABLE_PITCH_NOISE = True      # Enable pitch noise
        self.PITCH_NOISE_CENTS = 3.0        # Pitch noise depth

        # Amplitude modulation
        self.ENABLE_AMP = True
        self.AMP_EXPONENT = 0.7             # Amplitude curve exponent
        self.ENABLE_AMP_NOISE = True
        self.AMP_NOISE_DEPTH = 0.1          # Depth of amplitude noise

        # Chaotic noise field
        self.ENABLE_CHAOS_NOISE = True
        self.CHAOS_NOISE_RANDOM = 0.02      # Random jitter amount
        self.CHAOS_NOISE_SMOOTH = 200       # LPF smoothing window (samples)

        # Phase shift master switch
        self.ENABLE_PHASE_SHIFT = True      # Per‑voice phase offset master flag


        # -----------------------------
        # PITCH MODULATION
        # -----------------------------
        self.DETUNE_CENTS = 40.0          # Max chaotic detune in cents
        self.ENABLE_PITCH_NOISE = True    # Enable pitch noise
        self.PITCH_NOISE_CENTS = 3.0      # Pitch noise depth (cents)

        # -----------------------------
        # AMPLITUDE MODULATION
        # -----------------------------
        self.ENABLE_AMP = True
        self.AMP_EXPONENT = 0.7           # Amplitude curve exponent
        self.ENABLE_AMP_NOISE = True
        self.AMP_NOISE_DEPTH = 0.1        # Depth of amplitude noise

        # -----------------------------
        # CHAOTIC NOISE FIELD
        # -----------------------------
        self.ENABLE_CHAOS_NOISE = True
        self.CHAOS_NOISE_RANDOM = 0.02    # Random jitter amount
        self.CHAOS_NOISE_SMOOTH = 200     # LPF smoothing window (samples)

        # -----------------------------
        # PHASE SHIFT MASTER SWITCH
        # -----------------------------
        self.ENABLE_PHASE_SHIFT = True    # Per‑voice phase offset master flag

        # -----------------------------
        # MICRO INSTABILITY MODULE
        # -----------------------------
        self.MICRO_INSTABILITY_ON = True
        self.MICRO_INSTABILITY_DEPTH = 0.15      # 0.0 = no drift, 1.0 = wild
        self.MICRO_INSTABILITY_RATE = 0.05       # Hz or slow LFO rate
        self.MICRO_INSTABILITY_SEED = 12345      # reproducible drift

        # -----------------------------
        # BEHAVIOURAL MODULATION MODULE
        # -----------------------------
        self.BEHAVIOUR_MOD_ON = True
        self.BEHAVIOUR_MOD_DEPTH = 0.5           # overall modulation intensity
        self.BEHAVIOUR_MOD_SENSITIVITY = 0.7     # how reactive to attractor changes
        self.BEHAVIOUR_MOD_SMOOTHING = 0.2       # prevents sudden jumps

        # -----------------------------
        # GROOVE EMERGENCE MODULE
        # -----------------------------
        self.GROOVE_ON = True
        self.GROOVE_DEPTH = 0.4                  # how much groove is injected
        self.GROOVE_SWING = 0.1                  # timing bias
        self.GROOVE_VARIANCE = 0.05              # stochastic timing offsets
        self.GROOVE_RATE = 0.3                   # LFO or pulse cloud rate
