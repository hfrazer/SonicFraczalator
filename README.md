# SONICFRACZALATOR
A modular chaotic‑chord synthesizer built in Python.

The SONICFRACZALATOR is a fully modular, chaos‑driven chord engine that transforms strange attractors into evolving harmonic structures. It began life as a monolithic “Fractal‑Chords.py” experiment and has since grown into a clean, extensible instrument with:

- modular DSP pipeline
- per‑voice synthesis
- chaotic modulation
- timbre morphing
- stereo panning
- progress‑bar UX
- full WAV rendering
- future‑proof architecture ready for GUIs, presets, and live control

If you enjoy chaotic systems, generative harmony, or building instruments that feel alive, this project is for you.

---

## Features

- Rössler (or any) attractor drives pitch, timbre, amplitude, and panning
- Drop‑in attractor architecture — swap chaos systems with one line
- Chord engine with per‑voice base frequencies
- Per‑voice DSP chain:
  - oscillators
  - timbre morphing
  - amplitude shaping
  - chaotic noise
  - stereo panning
- Progress bars for attractor, voices, and stages
- Per‑voice render timing
- Modular file structure for future GUI / presets / MIDI
- WAV output + optional playback

---

## Project Structure

    SonicFraczalator/
    │
    ├── main.py                     # Entry point: render + write WAV + playback
    ├── params.py                   # All tweakable instrument parameters
    │
    ├── render_engine/
    │   ├── render_track.py         # Full track renderer (attractor → voices → mix)
    │   ├── mixdown.py              # Stereo summing + normalisation
    │
    ├── voices/
    │   ├── voice_engine.py         # Per‑voice DSP loop + progress bars
    │   ├── oscillators.py          # Sine, square, etc.
    │   ├── timbre.py               # Timbre morphing engine
    │   ├── panning.py              # Stereo panning engine
    │
    ├── harmony_engine/
    │   └── chord_engine.py         # Chord sequencing + per‑voice base frequencies
    │
    ├── sonic_animation_engine/
    │   ├── chaos_noise.py          # Chaotic noise generator
    │   ├── phase_shift.py          # Optional per‑voice phase shifting
    │   └── attractors/             # Drop‑in chaos systems
    │
    └── requirements.txt            # Dependencies








---

## Getting Started

### 1. Clone the repo

git clone https://github.com/hfrazer/SonicFraczalator.git (github.com in Bing)
cd SonicFraczalator

### 2. Create a virtual environment

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


### 3. Install dependencies

pip install -r requirements.txt


### 4. Run the engine

python main.py

You will see:

- attractor progress  
- per‑voice progress  
- per‑voice timing  
- mixdown  
- WAV writing  
- playback  

---

## Configuration

All parameters live in `params.py`.

Key ones include:

- TRACK_DUR_SECS — total render length  
- CHORD_DUR_SECS — how long each chord lasts  
- WAV_OUTPUT_PATH — where the file is written  
- DETUNE_CENTS, TIMBRE_DEPTH, PAN_DEPTH  
- ENABLE_PITCH_NOISE, ENABLE_TIMBRE, etc.  
- ATTRACTOR — choose your chaos system  
- CHAOS_GEARING — how fast the attractor evolves  

---

## Extending the Instrument

### Add a new attractor
Drop a file into: sonic_animation_engine/attractors/
Implement `.step()` returning `{x, y, z}`.

### Add a new timbre engine
Modify or extend: voices/timbre.py


### Add new oscillators
Add functions to:
voices/oscillators.py

### Add new chord logic
Modify: harmony_engine/chord_engine.py


---

## Example Output

The engine produces evolving, chaotic chord textures — somewhere between:

- generative ambient  
- unstable pads  
- drifting harmonic clouds  
- chaotic modulation experiments  

Perfect for sound design, ambient music, or algorithmic composition.

---

## License

MIT License — feel free to fork, remix, and build on it.
---

## Multiprocessing Architecture

SonicFraczalator uses Python's multiprocessing to accelerate rendering by splitting the audio into horizontal time chunks. Each chunk covers all voices for a short time interval (default: 5 seconds), maximizing CPU utilization and trying to keep progress reporting as responsive as possible.

- **Time Chunking:** The audio is divided into small, fixed-duration chunks (see `CHUNK_SIZE_SECONDS` in `params.py`). Each chunk is processed independently across all voices.
- **Stateless Workers:** Each worker process receives all the data it needs for its chunk, ensuring no shared state or race conditions.
- **Progress Reporting:** As each chunk completes, the main process receives a callback and updates at these intervals a 'smooth-as-possible', progress bar with ETA. Output from worker processes is suppressed to keep the progress bar clean.
- **Stages:** Progress bars are shown for attractor generation and for voice rendering, giving clear feedback on long renders.

This architecture ensures efficient parallelism, accurate progress feedback, and efficient and robust handling of large renders on multi-core systems.

---

## Troubleshooting

- If you do not see progress bars for attractor or voice rendering, ensure you are running the latest code. A bug in the progress bar logic was fixed in March 2026.
- All progress bars now update smoothly with progressively more accurate ETA. No configuration is needed.
- Output from worker processes is suppressed to prevent interference with the main progress bar.

## Changelog

- **2026-03:** Fixed progress bar logic so all bars (attractor, rendering voices) update correctly and smoothly.
- Suppressed all print statements from multiprocessing workers for clean output.
- Removed temporary test progress bar code from production.

---

## Contributing

Pull requests are welcome — especially:

- new attractors  
- new timbre engines  
- new chord systems  
- performance optimisations  
- GUI experiments  

---

## Author

Built by Hugh Frazer — Perth‑based creative coder, modular synth explorer, and chaos‑driven instrument designer.



