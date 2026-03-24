# params.py
# ---------------------------------------------------------------------------
# SONICFRACZALATOR — Complete Global Parameter Definitions
#
# This file merges:
#   • Legacy Fractal‑Chords.py parameters
#   • New Sonic Animation modules
#   • Modernised modular engine parameters
#
# Every parameter is documented and grouped by subsystem.
# ---------------------------------------------------------------------------

class VibeParams:
    def __init__(self):

        # -------------------------------------------------------------------
        # ATTRACTOR ENGINE
        # -------------------------------------------------------------------
        # --- Attractor selection ---
        self.ATTRACTOR = "aizawa"        # "rossler", "lorenz", "halvorsen", "aizawa", "thomas", etc.
        # --- Global chaos controls ---
        self.BASE_DT = 0.01                 # Base integration timestep
        self.CHAOS_GEARING = 1.1            # Speed multiplier for attractor
        # --- Seed for chaos / randomness ---
        import time
        self.SEED = int(time.time() * 1000) # Unique seed per render

        # --- Attractor-specific presets ---
        self.ATTRACTOR_PRESETS = {
            "lorenz":    {"dt": 0.01,  "scale": 1.0, "init": (0.1, 0.0, 0.0)},
            "rossler":   {"dt": 0.005, "scale": 1.0, "init": (0.1, 0.1, 0.1)},
            "halvorsen": {"dt": 0.001, "scale": 0.5, "init": (0.1, 0.0, 0.0)},
            "aizawa":    {"dt": 0.002, "scale": 0.3, "init": (0.1, 0.0, 0.0)},
            "thomas":    {"dt": 0.001,  "scale": 300.0, "init": (1.0, 1.0, 1.0)},
            # "thomas":    {"dt": 0.01,  "scale": 0.7, "init": (0.1, 0.1, 0.1)},  This one is too dampened 
        }
        # Optional attractor scaling/offsets
        self.CHAOS_SCALE_X = 1.0
        self.CHAOS_SCALE_Y = 1.0
        self.CHAOS_SCALE_Z = 1.0
        self.CHAOS_OFFSET_X = 0.0
        self.CHAOS_OFFSET_Y = 0.0
        self.CHAOS_OFFSET_Z = 0.0

        # -------------------------------------------------------------------
        # AUDIO ENGINE
        # -------------------------------------------------------------------
        self.SAMPLE_RATE = 44100        # Hz
        self.TRACK_DUR_SECS = 40        # Total render duration

        # -------------------------------------------------------------------
        # MULTIPROCESSING CHUNKING
        # -------------------------------------------------------------------
        self.CHUNK_SIZE_SECONDS = 5     # Duration of each processing chunk (seconds)

        # -------------------------------------------------------------------
        # OUTPUT
        # -------------------------------------------------------------------
        self.WAV_OUTPUT_PATH = r"C:\Temp\fancychord.wav"
        self.ENABLE_PLAYBACK = True

        # -------------------------------------------------------------------
        # PHASE SHIFT (per‑voice chaos lanes)
        # -------------------------------------------------------------------
        self.PHASE_SHIFT_MODE = "even"  # "even", "random", "golden_ratio"
        self.ENABLE_PHASE_SHIFT = True  # Master switch
        self.PHASE_SHIFT_AMOUNT = 0.1   # Depth of phase offset

        # -------------------------------------------------------------------
        # HARMONY ENGINE
        # -------------------------------------------------------------------
        self.CHORD_SEQUENCE = [
            [82.41, 110.00, 138.59, 146.83, 220.00],
            [55.00, 110.00, 138.59, 164.81, 277.18],
            [55.00, 110.00, 130.81, 164.81, 261.63],
            [49.00, 98.00, 130.81, 146.83, 261.63],
            [49.00, 98.00, 123.47, 146.83, 246.94],
        ]
        self.CHORD_DUR_SECS = 6.0       # Legacy default
        self.VOICE_COUNT = 5            # Number of voices per chord
        self.DROP2 = False              # Drop‑2 voicing

        # -------------------------------------------------------------------
        # TIMBRE ENGINE
        # -------------------------------------------------------------------
        self.ENABLE_TIMBRE = True
        self.TIMBRE_DEPTH = 1.0         # 0 = sine, 1 = full morph

        # -------------------------------------------------------------------
        # PANNING ENGINE
        # -------------------------------------------------------------------
        self.ENABLE_PAN = True
        self.PAN_DEPTH = 1.0            # 0 = mono, 1 = full stereo
        self.PAN_SMOOTHING = 0.1        # LPF smoothing

        # -------------------------------------------------------------------
        # LEGACY FRACTAL‑CHORDS SYNTH CONTROLS
        # -------------------------------------------------------------------

        # Pitch modulation
        self.DETUNE_CENTS = 40.0        # Max chaotic detune
        self.ENABLE_PITCH_NOISE = True
        self.PITCH_NOISE_CENTS = 3.0    # Pitch noise depth

        # Amplitude modulation
        self.ENABLE_AMP = True
        self.AMP_EXPONENT = 0.7         # Amplitude curve exponent
        self.ENABLE_AMP_NOISE = True
        self.AMP_NOISE_DEPTH = 0.1      # Depth of amplitude noise

        # Chaotic noise field
        self.ENABLE_CHAOS_NOISE = True
        self.CHAOS_NOISE_RANDOM = 0.02  # Random jitter
        self.CHAOS_NOISE_SMOOTH = 200   # LPF window (samples)

        # -------------------------------------------------------------------
        # MICRO INSTABILITY MODULE
        # -------------------------------------------------------------------
        self.MICRO_INSTABILITY_ON = True
        self.MICRO_INSTABILITY_DEPTH = 0.15
        self.MICRO_INSTABILITY_RATE = 0.05
        self.MICRO_INSTABILITY_SEED = 12345

        # -------------------------------------------------------------------
        # BEHAVIOURAL MODULATION MODULE
        # -------------------------------------------------------------------
        self.BEHAVIOUR_MOD_ON = True
        self.BEHAVIOUR_MOD_DEPTH = 0.5
        self.BEHAVIOUR_MOD_SENSITIVITY = 0.7
        self.BEHAVIOUR_MOD_SMOOTHING = 0.2

        # -------------------------------------------------------------------
        # GROOVE EMERGENCE MODULE
        # -------------------------------------------------------------------
        self.GROOVE_ON = True
        self.GROOVE_DEPTH = 0.4
        self.GROOVE_SWING = 0.1
        self.GROOVE_VARIANCE = 0.05
        self.GROOVE_RATE = 0.3

        # -------------------------------------------------------------------
        # ENVELOPES
        # -------------------------------------------------------------------
        self.ENV_ATTACK = 0.01
        self.ENV_DECAY = 0.2
        self.ENV_SUSTAIN = 0.8
        self.ENV_RELEASE = 0.5

        # -------------------------------------------------------------------
        # RENDERING / MIXDOWN
        # -------------------------------------------------------------------
        self.NORMALISE = True
        self.LIMITER = False
        self.STEM_OUTPUT = False
        self.PREVIEW_SECONDS = 5

        # -------------------------------------------------------------------
        # UTILS / TIMING
        # -------------------------------------------------------------------
        self.PROGRESS_UPDATE_RATE = 0.2
        self.PROFILE_VOICES = True
        self.RANDOM_SEED = 12345
