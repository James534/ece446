import numpy as np
from scipy.io import wavfile

# from https://mypianonotes.com/my-heart-will-go-on/
#   https://www.piano-keyboard-guide.com/my-heart-will-go-on-easy-piano-tutorial-titanic-theme-by-celine-dion/
notes = [
    # Every night in my dreams
    "E", "E", "E", "E", "D#", "E",
    "E", "D#", "E",     "F#", "G#", "F#",
    "E", "E", "E", "E", "D#", "E",      "E", "B",

    # Far across the distance
    "E", "E", "E", "D#", "E",
    "E", "D#", "E",     "F#", "G#", "F#",
    "E", "E", "E", "E", "D#", "E",      "E", "B",
]


note_file_mapping = {
    "G#":   "V2/Hole_1_G4#",
    "G":    "V2/Hole_2_G4",
    "F#":   "V2/Hole_3_F4#",
    "F":    "V2/Hole_4_F4",
    "E":    "V2/Hole_5_E4_v2",
    "D#":   "V2/Hole_6_D4#",
    "D":    "V2/Hole_7_D4",
    "B":    "V2/Hole_8_B3_v2",
}

def normalize(note_data, t_norm=1, rms_norm=10000):
    # 1 second = fs samples
    # normalize all notes to the same time
    # t_norm = 1          # seconds
    # rms_norm = 10000    # in float64 space

    # first convert recorded data to float64 space from int16 space
    note_data = note_data.astype(np.float64)

    # interpolate the data to be t_norm duration
    x_norm = np.linspace(0, t_norm, fs * t_norm)
    x_data = np.linspace(0, len(note_data)/fs, len(note_data))  # generate x from 0-file_length_in_seconds to use in interp
    norm_note_data = np.interp(x_norm, x_data, note_data)

    # normalize the data to rms_norm
    norm_note_data_rms = np.sqrt(np.mean(np.power(norm_note_data, 2)))
    norm_note_data *= rms_norm / norm_note_data_rms

    # save the data as int16
    norm_note_data = norm_note_data.astype(np.int16)
    return norm_note_data


# normalize all notes
normalized_notes = {}
for note in set(notes):
    fs, note_data = wavfile.read(note_file_mapping[note] + ".wav")
    print(f"Note: {note} \tfs: {fs}\tlen: {len(note_data)}\tdur: {len(note_data)/fs}")

    norm_note_data = normalize(note_data, t_norm=0.5)
    normalized_notes[note] = norm_note_data
    # wavfile.write("generated/" + note + ".wav", fs, norm_note_data)

song = np.array([])
space = np.zeros(int(0.1 * 44100))
for note in notes:
    cur_note = normalized_notes[note]

    song = np.concatenate((song, cur_note, space), axis=0)
song = song.astype(np.int16)
wavfile.write("generated/titanic.wav", 44100, song)
