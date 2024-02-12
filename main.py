
from pathlib import Path
from midi import generate_progression, generate_notes
import pygame
import time

# GLOBALS

KEYS = [
	# indices correspont to keys in semitones from C
    'C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'
]

TEMP_FILE_PATH = 'tmp.mid'


def play_midi(mid):
    # save cadence as temporary_midi_file
    mid.save(TEMP_FILE_PATH)

    # play midi
    pygame.mixer.music.load(TEMP_FILE_PATH, "mid")
    pygame.mixer.music.play()

    # play midi
    time.sleep(mid.length)

    # cleanup
    # Path(TEMP_FILE_PATH).unlink()
    return mid, TEMP_FILE_PATH


def play_cadence():
    
    key_idx, cadence_mid = generate_progression()

    print(f"We're in the key of {KEYS[key_idx]}")
    play_midi(cadence_mid)


def play_notes():
    notes, notes_mid = generate_notes()

    print(f"Notes are {notes}")
    play_midi(notes_mid)



def get_user_notes():
    user_input = input("What are the notes? ")
    user_notes = user_input.split(", ")

    return user_notes

def evaluate_guess(notes, user_notes):
    is_correct = notes.upper() == user_notes.upper()

    return is_correct

def play_round():
    pass



if __name__ == '__main__':

    # pick key
    # generate cadence
    pygame.init()
    
    while True:
        # show key
        # play cadence
        play_cadence()

        # choose number of notes
        # choose notes
        # play notes
        play_notes()

        # prompt for notes
        # evaluate input
        # rinse and repeat
        user_notes = get_user_notes()
            break
    pygame.quit()