from render_engine.render_track import TrackRenderer, print_render_header
from attractors import select_attractor        # ← NEW: clean import from __init__.py
from params import VibeParams
from harmony_engine.chord_engine import ChordEngine
from render_engine.mixdown import Mixdown
from scipy.io.wavfile import write

# ----------------------------------------------------------
# Parameters
# ----------------------------------------------------------
params = VibeParams()

# ----------------------------------------------------------
# Main entry point
# ----------------------------------------------------------
def main():
    print_render_header(params)

    # 1. Select attractor
    attractor = select_attractor(params.ATTRACTOR, params)

    # 2. Create track renderer
    renderer = TrackRenderer(params, attractor)

    # 3. Render full stereo track
    stereo = renderer.render(params.CHORD_SEQUENCE)

    # 4. Write WAV
    # Build descriptive output filename with timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    fname = (
        f"{params.ATTRACTOR}"
        f"-gear{params.CHAOS_GEARING}"
        f"-dt{params.BASE_DT}"
        f"-track{params.TRACK_DUR_SECS}"
        f"-chord{params.CHORD_DUR_SECS}"
        f"-voices{params.VOICE_COUNT}"
        f"-{timestamp}.wav"
    )

    output_path = f"C:/Temp/{fname}"
    write(output_path, params.SAMPLE_RATE, stereo)
    print(f"WAV file written to: {output_path}")

    # 4b. Write metadata JSON
    import json

    metadata = {
        "attractor": params.ATTRACTOR,
        "params": {
            "dt": params.BASE_DT,
            "chaos_gearing": params.CHAOS_GEARING,
            "track_duration": params.TRACK_DUR_SECS,
            "chord_duration": params.CHORD_DUR_SECS,
            "voices": params.VOICE_COUNT,
            "sample_rate": params.SAMPLE_RATE
        },
        "seed": params.SEED,
        "timestamp": timestamp,
        "version": "SONICFRACZALATOR 0.1"
    }

    json_path = f"C:/Temp/{fname.replace('.wav', '-metadata.json')}"
    with open(json_path, "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"Metadata written to: {json_path}")


    # 5. Playback
    import sounddevice as sd
    print("Render complete. Playing audio...")
    sd.play(stereo, params.SAMPLE_RATE)
    sd.wait()

    print("Done.")


if __name__ == "__main__":
    main()
