import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import random

"""
MIDI UTILS
"""

STARTING_NOTE = 48

CANDENCE = [
    # I - IV - V - I, formatted as tuple(Int, Int, Int, Int):
    ### the first Int is the bass (in semitones from the bass of the first chord)
    ### Each successive Int is semitones above the previous voice
    # this is just one example; I hope to add many others
    (0, 16, 3, 5),
    (5, 12, 4, 3),
    (7, 7, 5, 4),
    (0, 16, 3, 5)
]

KEYS = [
	# indices correspont to keys in semitones from C
    'C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'
]

VELOCITY = 64
QUARTER_NOTE = 480 # quarter note

# notes globals
NOTES_TEMPO = 60
MIN_NOTES = 2
MAX_NOTES = 2
RANGE_MIN = 36
RANGE_MAX = 72


def generate_meta_midi(tempo_bpm, key_idx):
    """
    create mido.MidiFile object with meta information
    """
    # Create a new MIDI file
    mid = MidiFile()

    # Create a MIDI track
    track = MidiTrack()
    mid.tracks.append(track)

    tempo = mido.bpm2tempo(tempo_bpm)  # Microseconds per beat
    track.append(MetaMessage('set_tempo', tempo=tempo))
    track.append(MetaMessage('key_signature', key=KEYS[key_idx], time=0))

    # time signature (always 4/4)
    track.append(MetaMessage('time_signature', numerator=4, denominator=4))

    return mid


def progression_to_midi(mid, progression, starting_note):
    """
    write a progression to midi
    """
    track = MidiTrack()
    mid.tracks.append(track)

    for i, chord in enumerate(progression):
		# chord is a tuple of notes, indicated as intervals from bass note of first chord
        note = starting_note
        for interval in chord:
            note += interval
            track.append(Message('note_on', note=note, velocity=VELOCITY, time=0))

        # advance to half note and release first note
        duration = 2*QUARTER_NOTE if (i == len(chord)-1) else QUARTER_NOTE
        track.append(Message('note_off', note=starting_note+chord[0], velocity=0, time=duration))

        note = starting_note
        for interval in chord:
            note += interval
            track.append(Message('note_off', note=note, velocity=0, time=0))
        
    # add 1/2 note rest at the end of the track
    track.append(MetaMessage('end_of_track', time=3*QUARTER_NOTE))
        
    return mid


def generate_progression(tempo_bpm=None, key_idx=None):
    """
    choose key, tempo, starting note
    """

    # randomize meta info if not predetermined
    if not tempo_bpm:
        tempo_bpm = random.randint(70, 130)
    if not key_idx:
        key_idx = random.choice(range(12))

    # default starting note is 48
    starting_interval = random.choice([key_idx, key_idx-12])
    starting_note = STARTING_NOTE + starting_interval

    mid = generate_meta_midi(tempo_bpm, key_idx)
    mid = progression_to_midi(mid, CANDENCE, starting_note)

    return key_idx, mid


def generate_notes():
    """
    Generate notes to be heard against starting cadence
    """
    mid = generate_meta_midi(NOTES_TEMPO, 0)
    
    # to be altered
    num_notes = random.choice(range(MIN_NOTES, MAX_NOTES+1))
    # choose pitch classes
    pitch_class_ids = random.sample(range(12), num_notes)
    pitches = [random.choice(get_pitches_in_range(pitch, RANGE_MIN, RANGE_MAX)) for pitch in pitch_class_ids]

    # turn pitches into "progression" tuple
    pitches.sort()
    starting_note = pitches[0]
    progression = [pitches[i]-pitches[max(0, i-1)] for i in range(len(pitches))]

    # generate midi from pitches, 60 bpm and no key signature
    mid = generate_meta_midi(NOTES_TEMPO, 0)
    mid = progression_to_midi(mid, [tuple(progression)], starting_note)

    return pitch_class_ids, mid


def get_pitches_in_range(pitch, min, max):
    """
    Find all octave transpositions of `pitch` that lie between the range [min, max)
    """
    pitch_class = pitch % 12
    
    current_pitch = pitch_class
    available_pitches = []
    
    while current_pitch < max:
        if current_pitch >= min:
            available_pitches.append(current_pitch)
        current_pitch += 12
    
    return available_pitches