
from pathlib import Path
from midi import generate_progression, generate_notes
import mido
import pygame
import time

# GLOBALS

KEYS = [
	# indices correspont to keys in semitones from C
    'C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'
]

# spellings of notes for reference
NOTES = [
    'c', 'db', 'd', 'eb', 'e', 'f', 'f#', 'g', 'ab', 'a', 'bb', 'b'
]
NOTES_ALT = [
    'b#', 'c#', 'd', 'd#', 'fb', 'e#', 'gb', 'g', 'g#', 'a', 'a#', 'cb'
    ]

TEMP_FILE_PATH = lambda name: Path(f'tmp_{name}.mid')


def play_midi_from_file(mid_file_path, mid: mido.MidiFile):
    """
    Takes path and mido.MidiFile object. Redundant but
    object is needed to evaluate length in time
    """
    # play midi
    pygame.mixer.music.load(mid_file_path, "mid")
    pygame.mixer.music.play()

    # play midi
    time.sleep(mid.length)


def get_idx_from_note_name(note_name):

    try:
        if note_name.lower() in NOTES:
            return NOTES.index(note_name.lower())
        elif note_name.lower() in NOTES_ALT:
            return NOTES_ALT.index(note_name.lower())
    except ValueError:
        return None


def get_user_notes(user_input):
    
    user_notes = user_input.lower().split(", ")

    return set([get_idx_from_note_name(note) for note in user_notes])


if __name__ == '__main__':

    # pick key
    # generate cadence
    pygame.init()
    
    while True:
        # generate MIDI and get meta info
        key_idx, cadence_mid = generate_progression()
        notes, notes_mid = generate_notes()

        # save MIDI as temp files
        cadence_mid.save(TEMP_FILE_PATH("key"))
        notes_mid.save(TEMP_FILE_PATH("notes"))

        # establish key
        print(f"We're in the key of {KEYS[key_idx]}")
        
        # play midi
        play_midi_from_file(TEMP_FILE_PATH("key"), cadence_mid)
        play_midi_from_file(TEMP_FILE_PATH("notes"), notes_mid)

        user_notes = set()

        while user_notes != set(notes):
            # prompt for input
            user_input = input("What are the notes? ")
            user_notes = get_user_notes(user_input)
        
            if user_notes != set(notes):
                # incorrect -- replay
                print("Try again :(")
    
        # correct -- move on
        print("you got it!")
        # cleanup
        TEMP_FILE_PATH("key").unlink()
        TEMP_FILE_PATH("notes").unlink()
    
    pygame.quit()