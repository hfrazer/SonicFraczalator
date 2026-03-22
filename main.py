from render_engine.render_track import TrackRenderer
from attractors.rossler import RosslerAttractor
from attractors.lorenz import LorenzAttractor
from attractors.halvorsen import HalvorsenAttractor
from harmony_engine.chord_engine import ChordEngine
from params import VibeParams
from render_engine.mixdown import Mixdown

params = VibeParams()
def select_attractor(name, params):
    name = name.lower()
    dt = params.BASE_DT * params.CHAOS_GEARING

    if name == "rossler":
        return RosslerAttractor(dt=dt)
    elif name == "lorenz":
        return LorenzAttractor(dt=dt)
    elif name == "halvorsen":
        return HalvorsenAttractor(dt=dt)
    else:
        raise ValueError(f"Unknown attractor: {name}")

def main():
    print("SONICFRACZALATOR — full track render starting...")

    # 1. Select attractor
    attractor = select_attractor(params.ATTRACTOR, params)

    # 2. Create track renderer
    renderer = TrackRenderer(params, attractor)

    # 3. Render full stereo track
    stereo = renderer.render(params.CHORD_SEQUENCE)

    # --- Write WAV file ---
    from scipy.io.wavfile import write
    write(params.WAV_OUTPUT_PATH, params.SAMPLE_RATE, stereo)
    print(f"WAV file written to: {params.WAV_OUTPUT_PATH}")



    # 4. Playback
    import sounddevice as sd
    print("Render complete. Playing audio...")
    sd.play(stereo, params.SAMPLE_RATE)
    sd.wait()

    print("Done.")



if __name__ == "__main__":
    main()
