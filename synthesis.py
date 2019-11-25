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

note_midi_mapping = {
    "G#":   68,   # G4#
    "G":    67,   # G4
    "F#":   66,   # F4#
    "F":    65,   # F4
    "E":    64,   # E4
    "D#":   63,   # D4#
    "D":    62,   # D4
    "B":    59,   # B3
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

    norm_note_data = normalize(note_data, t_norm=1)
    normalized_notes[note] = norm_note_data
    # wavfile.write("generated/" + note + ".wav", fs, norm_note_data)

sampling_rate = 44100
for note in set(notes):
    cur_note = normalized_notes[note]

#%%
import mido

core_note_mapping = {
    2:"D",
    3:"D#",
    4:"E",
    5:"F",
    6:"F#",
    7:"G",
    8:"G#",
    11:"B",
}

mid = mido.MidiFile("heart_will_go_on_filtered.mid")
song = np.array([0])
current_time = 0
last_msg = None
for msg in mid.play():
    if msg.type is not "note_on" and msg.type is not "note_off":
        continue
    if msg.channel != 0:
        continue
    if msg.type is "note_off":
        print("\t", msg)
    else:
        print(msg)

    if last_msg is not None:
        note_dur_samples = int(msg.time * sampling_rate)
        # msg.time = duration of that note
        if last_msg.type is "note_on":
            core_note_id = last_msg.note % 12
            norm_note = normalized_notes[core_note_mapping[core_note_id]]
            note = normalize(norm_note, t_norm=msg.time)

            song = np.concatenate((song, note))
        elif last_msg.type is "note_off":
            zeros = np.zeros(note_dur_samples)
            song = np.concatenate((song, zeros))

        current_time += int(msg.time * sampling_rate)

    last_msg = msg

song = song.astype(np.int16)
wavfile.write("generated/titanic.wav", sampling_rate, song)

