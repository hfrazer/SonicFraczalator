# PARAMETERS

A human-readable guide to every parameter in the SONICFRACZALATOR.
This document explains what each control does, why it matters, and how it shapes the sound.

---------------------------------------------------------------------

## CHAOS / ATTRACTOR ENGINE

ATTRACTOR  
    Chooses the chaotic system that drives the instrument. Different attractors
    create different shapes of motion, which translate into different musical
    behaviours.

BASE_DT  
    The raw integration timestep. Smaller values produce smoother, slower chaos;
    larger values produce sharper, more jagged motion.

CHAOS_GEARING  
    Speeds up or slows down the attractor relative to audio time. Low gearing
    gives slow drifting pads; high gearing gives twitchy, unstable modulation.

CHAOS_SCALE_X / CHAOS_SCALE_Y / CHAOS_SCALE_Z  
    How strongly each attractor axis influences the synth. Scaling X might make
    pitch more wild; scaling Z might make timbre more dramatic.

CHAOS_OFFSET_X / CHAOS_OFFSET_Y / CHAOS_OFFSET_Z  
    Shifts the attractor's centre. Useful for biasing modulation in a particular
    direction.

---------------------------------------------------------------------

## AUDIO ENGINE

SAMPLE_RATE  
    Standard audio sample rate. Higher values give more fidelity at higher CPU cost.

TRACK_DUR_SECS  
    Total duration of the rendered track.

---------------------------------------------------------------------

## OUTPUT

WAV_OUTPUT_PATH  
    Where the final WAV file is written.

ENABLE_PLAYBACK  
    If true, the engine plays the result after rendering.

---------------------------------------------------------------------

## PHASE SHIFT ENGINE

PHASE_SHIFT_MODE  
    How per-voice phase offsets are assigned.
    Options: even, random, golden_ratio.

ENABLE_PHASE_SHIFT  
    Master switch for phase shifting.

PHASE_SHIFT_AMOUNT  
    Depth of the phase offsets. Small values give subtle shimmer; large values
    give swirling chorus-like motion.

---------------------------------------------------------------------

## HARMONY ENGINE

CHORD_SEQUENCE  
    Your harmonic progression. Each chord is a list of base frequencies for each
    voice.

CHORD_DUR_SECS  
    How long each chord lasts before switching.

VOICE_COUNT  
    Number of voices per chord.

DROP2  
    Classic jazz voicing trick that drops the second-highest note by an octave
    for smoother spacing.

---------------------------------------------------------------------

## TIMBRE ENGINE

ENABLE_TIMBRE  
    Turns timbre morphing on or off.

TIMBRE_DEPTH  
    How far the timbre morphing goes.
    0 = pure sine
    1 = full morph (square-like, harmonically rich)

---------------------------------------------------------------------

## PANNING ENGINE

ENABLE_PAN  
    Turns stereo panning on or off.

PAN_DEPTH  
    How wide the stereo field is.
    0 = mono
    1 = full left/right spread

PAN_SMOOTHING  
    How slowly panning changes. Higher smoothing gives gentle drift; lower
    smoothing gives jittery stereo motion.

---------------------------------------------------------------------

## PITCH MODULATION

DETUNE_CENTS  
    Maximum chaotic detune applied to each voice. Creates thickness, instability,
    or wildness.

ENABLE_PITCH_NOISE  
    Turns pitch jitter on or off.

PITCH_NOISE_CENTS  
    Depth of pitch noise. Small values give analog drift; large values give
    unstable, broken-oscillator effects.

---------------------------------------------------------------------

## AMPLITUDE MODULATION

ENABLE_AMP  
    Turns amplitude shaping on or off.

AMP_EXPONENT  
    Shapes the amplitude curve.
    Less than 1 = softer, rounder
    Greater than 1 = sharper, more percussive

ENABLE_AMP_NOISE  
    Turns amplitude jitter on or off.

AMP_NOISE_DEPTH  
    How much chaotic noise affects loudness.

---------------------------------------------------------------------

## CHAOTIC NOISE FIELD

ENABLE_CHAOS_NOISE  
    Master switch for the chaotic noise layer.

CHAOS_NOISE_RANDOM  
    How much random jitter is injected into the noise field.

CHAOS_NOISE_SMOOTH  
    How much smoothing is applied.
    Large values give slow drifting noise; small values give grainy, unstable noise.

---------------------------------------------------------------------

## MICRO INSTABILITY MODULE

Simulates the "alive", unstable behaviour of analog circuits.

MICRO_INSTABILITY_ON  
    Master switch.

MICRO_INSTABILITY_DEPTH  
    How far parameters drift over time.

MICRO_INSTABILITY_RATE  
    How fast the drift happens.

MICRO_INSTABILITY_SEED  
    Seed for reproducible drift patterns.

---------------------------------------------------------------------

## BEHAVIOURAL MODULATION MODULE

Makes the synth react to the attractor's behaviour, not just follow it.

BEHAVIOUR_MOD_ON  
    Master switch.

BEHAVIOUR_MOD_DEPTH  
    How strongly behaviour affects modulation.

BEHAVIOUR_MOD_SENSITIVITY  
    How reactive the system is to sudden attractor changes.

BEHAVIOUR_MOD_SMOOTHING  
    Prevents abrupt jumps and makes behaviour feel organic.

---------------------------------------------------------------------

## GROOVE EMERGENCE MODULE

Injects timing irregularities and rhythmic feel.

GROOVE_ON  
    Master switch.

GROOVE_DEPTH  
    How strong the groove effect is.

GROOVE_SWING  
    Biases timing forward/backward like classic swing.

GROOVE_VARIANCE  
    Random timing offsets for humanisation.

GROOVE_RATE  
    Rate of the underlying groove LFO or pulse cloud.

---------------------------------------------------------------------

## ENVELOPES

ENV_ATTACK  
    Fade-in time.

ENV_DECAY  
    Time to fall from peak to sustain.

ENV_SUSTAIN  
    Steady-state level.

ENV_RELEASE  
    Fade-out time.

---------------------------------------------------------------------

## RENDERING / MIXDOWN

NORMALISE  
    Brings the final mix to full scale.

LIMITER  
    Soft clipping to prevent overloads.

STEM_OUTPUT  
    If true, writes each voice to its own WAV file.

PREVIEW_SECONDS  
    Length of preview render.

---------------------------------------------------------------------

## UTILS / TIMING

PROGRESS_UPDATE_RATE  
    How often progress bars update.

PROFILE_VOICES  
    Prints per-voice render times.

RANDOM_SEED  
    For reproducible renders.

---------------------------------------------------------------------
