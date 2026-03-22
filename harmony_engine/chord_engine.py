# chord_engine.py
# Harmony engine for SONICFRACZALATOR
# Ports the legacy CHORD_SEQUENCE + chord switching logic

class ChordEngine:
    def __init__(self, chord_sequence, chord_duration_secs, sample_rate):
        self.chord_sequence = chord_sequence
        self.chord_duration_secs = chord_duration_secs
        self.sample_rate = sample_rate

        self.num_chords = len(chord_sequence)
        self.num_voices = len(chord_sequence[0])
        self.samples_per_chord = int(chord_duration_secs * sample_rate)

    def get_base_freq(self, sample_index, voice_index):
        """
        Return the base frequency for this voice at this sample index.
        Matches legacy behaviour exactly.
        """
        chord_index = (sample_index // self.samples_per_chord) % self.num_chords
        return self.chord_sequence[chord_index][voice_index]
