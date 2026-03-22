# ===============================================================
# FRACTAL CHORD RENDERER — Rössler / Alttractor Sonification
#
# To Run:
#   1. Save this file as:  Fract-Chords.py
#   2. Open a command prompt and navigate to the folder:
#        cd C:\Temp
#   3. Example usage:
#        python Fract-Chords.py -a rossler -g 1.5 -c 4 -t 30
#
# Notes:
#   • chaos_gearing, chord_dur_secs, track_dur_secs, and attractor are CLI adjustable.
#   • All other synthesis parameters live in the PARAMS database.
#   • Use --list-parameters to view all synthesis controls.
#   • Rendering can take several minutes depending on duration.
#   • A progress bar with ETA will show rendering progress.
# ===============================================================

import numpy as np
from scipy.io.wavfile import write
import argparse
import os
import time
import sys

# ===============================================================
# PARAMETER DATABASE — single source of truth
# ===============================================================

PARAMS = {
    # Output
    "WAV_OUTPUT_PATH": {
        "value": r"C:\Temp\rossler_chord.wav",
        "default": r"C:\Temp\rossler_chord.wav",
        "desc": "Output WAV file location"
    },
    "SAMPLE_RATE": {
        "value": 44100,
        "default": 44100,
        "desc": "Audio sample rate"
    },
    "TRACK_DUR_SECS": {
        "value": 10.0,
        "default": 10.0,
        "desc": "Total audio duration (seconds)"
    },

    # Chaos engine (Rössler)
    "BASE_DT": {
        "value": 0.01,
        "default": 0.01,
        "desc": "Integrator timestep"
    },
    "ROSSLER_A": {
        "value": 0.23,
        "default": 0.23,
        "desc": "Rössler parameter A"
    },
    "ROSSLER_B": {
        "value": 0.18,
        "default": 0.18,
        "desc": "Rössler parameter B"
    },
    "ROSSLER_C": {
        "value": 5.2,
        "default": 5.2,
        "desc": "Rössler parameter C"
    },

    # Lorenz parameters
    "LORENZ_SIGMA": {
        "value": 10.0,
        "default": 10.0,
        "desc": "Lorenz sigma"
    },
    "LORENZ_RHO": {
        "value": 28.0,
        "default": 28.0,
        "desc": "Lorenz rho"
    },
    "LORENZ_BETA": {
        "value": 8.0 / 3.0,
        "default": 8.0 / 3.0,
        "desc": "Lorenz beta"
    },

    # Halvorsen parameter
    "HALVORSEN_A": {
        "value": 1.4,
        "default": 1.4,
        "desc": "Halvorsen parameter a"
    },

    # Per-voice chaos
    "ENABLE_PHASE_SHIFT": {
        "value": True,
        "default": True,
        "desc": "Enable per-voice phase offset"
    },
    "PHASE_SHIFT_MODE": {
        "value": "even",
        "default": "even",
        "desc": "Phase shift mode (even/random/golden_ratio)"
    },

    # Pitch modulation
    "DETUNE_CENTS": {
        "value": 40.0,
        "default": 40.0,
        "desc": "Max chaotic detune in cents"
    },
    "ENABLE_PITCH_NOISE": {
        "value": True,
        "default": True,
        "desc": "Enable pitch noise"
    },
    "PITCH_NOISE_CENTS": {
        "value": 3.0,
        "default": 3.0,
        "desc": "Pitch noise depth"
    },

    # Timbre modulation
    "ENABLE_TIMBRE": {
        "value": True,
        "default": True,
        "desc": "Enable sine→square morphing"
    },
    "TIMBRE_DEPTH": {
        "value": 1.0,
        "default": 1.0,
        "desc": "Depth of timbre modulation"
    },

    # Amplitude modulation
    "ENABLE_AMP": {
        "value": True,
        "default": True,
        "desc": "Enable amplitude shaping"
    },
    "AMP_EXPONENT": {
        "value": 0.7,
        "default": 0.7,
        "desc": "Amplitude curve exponent"
    },
    "ENABLE_AMP_NOISE": {
        "value": True,
        "default": True,
        "desc": "Enable amplitude noise"
    },
    "AMP_NOISE_DEPTH": {
        "value": 0.1,
        "default": 0.1,
        "desc": "Depth of amplitude noise"
    },

    # Stereo modulation
    "ENABLE_PAN": {
        "value": True,
        "default": True,
        "desc": "Enable stereo panning"
    },
    "PAN_DEPTH": {
        "value": 1.0,
        "default": 1.0,
        "desc": "Panning depth"
    },

    # Chaotic noise generator
    "ENABLE_CHAOS_NOISE": {
        "value": True,
        "default": True,
        "desc": "Enable chaotic noise field"
    },
    "CHAOS_NOISE_RANDOM": {
        "value": 0.02,
        "default": 0.02,
        "desc": "Random jitter amount"
    },
    "CHAOS_NOISE_SMOOTH": {
        "value": 200,
        "default": 200,
        "desc": "LPF smoothing window"
    },

    # Command-line parameters
    "CHAOS_GEARING": {
        "value": 1.0,
        "default": 1.0,
        "desc": "Time-scaling factor for chaotic attractor (like gear ratio)"
    },
    "CHORD_DUR_SECS": {
        "value": 6.0,
        "default": 6.0,
        "desc": "Seconds before switching chords"
    },
    "ATTRACTOR": {
        "value": "rossler",
        "default": "rossler",
        "desc": "Which chaotic attractor to use (rossler/lorenz/halvorsen)"
    },
}

# ===============================================================
# CHORD SEQUENCE (structured musical data, not a parameter)
# ===============================================================

CHORD_SEQUENCE = [
    [82.41, 110.00, 138.59, 146.83, 220.00],
    [55.00, 110.00, 138.59, 164.81, 277.18],
    [55.00, 110.00, 130.81, 164.81, 261.63],
    [49.00, 98.00, 130.81, 146.83, 261.63],
    [49.00, 98.00, 123.47, 146.83, 246.94],
]

# ===============================================================
# Command-line parameters
# ===============================================================

parser = argparse.ArgumentParser(
    usage=(
        "python Fract-Chords.py\n"
        "       [-a ATTRACTOR | --attractor ATTRACTOR]\n"
        "       [-g CHAOS_GEARING | --chaos_gearing CHAOS_GEARING]\n"
        "       [-c CHORD_DUR_SECS | --chord_dur_secs CHORD_DUR_SECS]\n"
        "       [-t TRACK_DUR_SECS | --track_dur_secs TRACK_DUR_SECS]\n"
        "       [--list-parameters]"
    ),
    description=(
        "Rössler / Alttractor Fractal Chord Renderer\n"
        "\n"
        "Attractors:\n"
        "  rossler    Smooth, spiralling, breathing\n"
        "  lorenz     Storm-like, dramatic swings\n"
        "  halvorsen  Crunchy, noisy, glitch-friendly\n"
        "\n"
        "Example:\n"
        "  python Fract-Chords.py -a rossler -g 1.5 -c 4 -t 30\n"
        "\n"
        "All other synthesis controls live in the PARAMS database."
    ),
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument(
    "-a", "--attractor",
    type=str,
    default="rossler",
    help="Which attractor to use (rossler/lorenz/halvorsen)"
)
parser.add_argument("-g", "--chaos_gearing", type=float, default=1.0)
parser.add_argument("-c", "--chord_dur_secs", type=float, default=6.0)
parser.add_argument(
    "-t", "--track_dur_secs",
    type=float,
    default=None,
    help="Override total track duration in seconds"
)
parser.add_argument("--list-parameters", action="store_true")

args = parser.parse_args()

# Inject CLI values into PARAMS
PARAMS["ATTRACTOR"]["value"] = args.attractor.lower()
PARAMS["CHAOS_GEARING"]["value"] = args.chaos_gearing
PARAMS["CHORD_DUR_SECS"]["value"] = args.chord_dur_secs

# Override track duration if provided
if args.track_dur_secs is not None:
    PARAMS["TRACK_DUR_SECS"]["value"] = args.track_dur_secs

# ===============================================================
# Extract PARAMS into globals for clean DSP code
# ===============================================================

for name, p in PARAMS.items():
    globals()[name] = p["value"]

# ===============================================================
# Parameter listing function
# ===============================================================

def list_parameters():
    print("\n" + "="*60)
    print("SYNTHESIS PARAMETERS (PARAMS DATABASE)")
    print("="*60)

    for name, p in PARAMS.items():
        print(f"{name:22} = {p['value']!r:<12} (default: {p['default']!r})   # {p['desc']}")

    print("\nChord sequence:")
    print(f"  {len(CHORD_SEQUENCE)} chords × {len(CHORD_SEQUENCE[0])} voices")

    print("\nDone.\n")
    sys.exit(0)

if args.list_parameters:
    list_parameters()

# ===============================================================
# Startup summary
# ===============================================================

def report_startup():
    print("\n" + "="*60)
    print(f"Generating a {TRACK_DUR_SECS} second track to:")
    print(f"  {WAV_OUTPUT_PATH}")
    print("="*60)
    print(f"Attractor: {ATTRACTOR}")
    print("For editable python code parameter help, run with:")
    print("  --list-parameters")
    print("="*60)

    altered = []
    for name, p in PARAMS.items():
        if p["value"] != p["default"]:
            altered.append(name)

    if altered:
        print("\nUsing altered parameters:")
        for name in altered:
            p = PARAMS[name]
            print(f"  {name:22} = {p['value']!r:<12} (default: {p['default']!r})")
    else:
        print("\nAll synthesis parameters are at default values.")

    print("\nChord sequence:")
    print(f"  {len(CHORD_SEQUENCE)} chords × {len(CHORD_SEQUENCE[0])} voices")

    print("="*60 + "\n")

report_startup()

# ===============================================================
# Progress bar + ETA
# ===============================================================

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

def announce(msg):
    print("\n" + "="*60)
    print(msg)
    print("="*60)

# ===============================================================
# Helper functions
# ===============================================================

def cents_to_ratio(c):
    return 2.0 ** (c / 1200.0)

def norm(v):
    v = v - v.min()
    return v / (v.max() - v.min() + 1e-9)

# ===============================================================
# Attractor step functions
# ===============================================================

def step_rossler(x, y, z, dt):
    dx = -y - z
    dy = x + ROSSLER_A * y
    dz = ROSSLER_B + z * (x - ROSSLER_C)
    return x + dx * dt, y + dy * dt, z + dz * dt

def step_lorenz(x, y, z, dt):
    dx = LORENZ_SIGMA * (y - x)
    dy = x * (LORENZ_RHO - z) - y
    dz = x * y - LORENZ_BETA * z
    return x + dx * dt, y + dy * dt, z + dz * dt

def step_halvorsen(x, y, z, dt):
    dx = -HALVORSEN_A * x - 4 * y - 4 * z - y * y
    dy = -HALVORSEN_A * y - 4 * z - 4 * x - z * z
    dz = -HALVORSEN_A * z - 4 * x - 4 * y - x * x
    return x + dx * dt, y + dy * dt, z + dz * dt

def select_attractor(name):
    name = name.lower()
    if name == "rossler":
        return step_rossler
    elif name == "lorenz":
        return step_lorenz
    elif name == "halvorsen":
        return step_halvorsen
    else:
        raise ValueError(f"Unknown attractor: {name}")

# ===============================================================
# 1. Generate trajectory from selected attractor
# ===============================================================

step = select_attractor(ATTRACTOR)

num_steps = int(TRACK_DUR_SECS * SAMPLE_RATE * BASE_DT * CHAOS_GEARING)

x = 0.8
y = 0.02
z = 0.5

xs, ys, zs = [], [], []

announce(f"1. Generating {ATTRACTOR} trajectory")
start = time.time()

dt = BASE_DT * CHAOS_GEARING

for i in range(num_steps):
    x, y, z = step(x, y, z, dt)

    xs.append(x)
    ys.append(y)
    zs.append(z)

    progress_bar("Attractor", i, num_steps)

print(f"Completed in {time.time() - start:.2f} seconds.")

xs = norm(np.array(xs))
ys = norm(np.array(ys))
zs = norm(np.array(zs))

# ===============================================================
# 2. Resample to audio rate
# ===============================================================

num_samples = int(TRACK_DUR_SECS * SAMPLE_RATE)
t_control = np.linspace(0, 1, len(xs), endpoint=False)
t_audio   = np.linspace(0, 1, num_samples, endpoint=False)

X = np.interp(t_audio, t_control, xs)
Y = np.interp(t_audio, t_control, ys)
Z = np.interp(t_audio, t_control, zs)

# ===============================================================
# 3. Chaotic noise generator
# ===============================================================

announce("3. Building chaotic noise field")
start = time.time()

if ENABLE_CHAOS_NOISE:
    dX = np.abs(np.diff(X, prepend=X[0]))
    dY = np.abs(np.diff(Y, prepend=Y[0]))
    dZ = np.abs(np.diff(Z, prepend=Z[0]))

    chaos_noise = norm((dX + dY + dZ) / 3.0)
    chaos_noise += CHAOS_NOISE_RANDOM * np.random.randn(len(chaos_noise))

    kernel = np.ones(CHAOS_NOISE_SMOOTH) / CHAOS_NOISE_SMOOTH
    chaos_noise = np.convolve(chaos_noise, kernel, mode="same")
    chaos_noise = norm(chaos_noise)
else:
    chaos_noise = np.zeros_like(X)

print(f"Completed in {time.time() - start:.2f} seconds.")

# ===============================================================
# 4. Phase-shifted chaotic lanes
# ===============================================================

voices = []
N = len(X)
num_voices = len(CHORD_SEQUENCE[0])

for i in range(num_voices):

    if PHASE_SHIFT_MODE == "even":
        shift = int((i / num_voices) * N)
    elif PHASE_SHIFT_MODE == "random":
        shift = np.random.randint(0, N)
    elif PHASE_SHIFT_MODE == "golden_ratio":
        phi = (np.sqrt(5) - 1) / 2
        shift = int((i * phi % 1) * N)

    Xi = np.roll(X, shift)
    Yi = np.roll(Y, shift)
    Zi = np.roll(Z, shift)

    voices.append((Xi, Yi, Zi))

# ===============================================================
# 5. Build each voice
# ===============================================================

announce("5. Rendering voices")

left = np.zeros(num_samples, dtype=np.float32)
right = np.zeros(num_samples, dtype=np.float32)

samples_per_chord = int(CHORD_DUR_SECS * SAMPLE_RATE)
num_chords = len(CHORD_SEQUENCE)

for v, (Xi, Yi, Zi) in enumerate(voices):
    print(f"\n--- Voice {v+1}/{num_voices} ---")
    start = time.time()

    voice_signal = np.zeros(num_samples, dtype=np.float32)
    phase = 0.0

    for i in range(num_samples):

        chord_index = (i // samples_per_chord) % num_chords
        base_freq = CHORD_SEQUENCE[chord_index][v]

        cents = (Xi[i] * 2 - 1) * DETUNE_CENTS
        if ENABLE_PITCH_NOISE:
            cents += (chaos_noise[i] * 2 - 1) * PITCH_NOISE_CENTS

        freq = base_freq * cents_to_ratio(cents)

        phase += 2 * np.pi * freq / SAMPLE_RATE
        sine = np.sin(phase)
        square = np.sign(sine) if sine != 0 else 1.0

        if ENABLE_TIMBRE:
            timbre = TIMBRE_DEPTH * np.abs(np.sin(Yi[i] * np.pi))
            sample = (1 - timbre) * sine + timbre * square
        else:
            sample = sine

        amp = Zi[i] ** AMP_EXPONENT if ENABLE_AMP else 1.0
        if ENABLE_AMP_NOISE:
            amp *= (1 + AMP_NOISE_DEPTH * (chaos_noise[i] - 0.5))

        voice_signal[i] = sample * amp

        progress_bar(f"Voice {v+1}", i, num_samples)

    print(f"Voice {v+1} complete in {time.time() - start:.2f} seconds.")

    pan = PAN_DEPTH * np.sin((Xi + Yi) * np.pi * 2) if ENABLE_PAN else 0.0
    left  += voice_signal * (0.5 * (1 - pan))
    right += voice_signal * (0.5 * (1 + pan))

# ===============================================================
# 6. Normalise + write
# ===============================================================

announce("6. Normalising + writing WAV file")

peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
if peak > 0:
    left  /= peak * 1.01
    right /= peak * 1.01

stereo = np.stack([left, right], axis=1)

os.makedirs(os.path.dirname(WAV_OUTPUT_PATH), exist_ok=True)
write(WAV_OUTPUT_PATH, SAMPLE_RATE, stereo.astype(np.float32))

print(f"Done! Output written to:\n{WAV_OUTPUT_PATH}")
