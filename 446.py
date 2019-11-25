import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import numpy as np
from scipy import signal
from scipy import optimize
import colorsys

# %%

# load the data
# fs, data = wavfile.read('flute_cover_holes_2.wav')
# print("fs", fs, "data len", len(data))
# print("max", max(data), "min", min(data))

max_freq_show = 1000
def do_fft(data):
    # calculate fourier transform (complex numbers list)
    freq_data = fft(data, fs)
    freq_data_len = len(freq_data)//2
    abs_freqs = abs(freq_data[:freq_data_len])

    k = np.arange(len(abs_freqs))
    T = len(data)/fs  # where fs is the sampling frequency
    freqLabel = k/T

    # print top freqs

    # show_freqs = 5
    # sorted_freqs = np.argsort(abs_freqs)
    # for i in sorted_freqs[-show_freqs:]:
    #     print(i, abs_freqs[i])
    return abs_freqs

"""
    Hole  0: 3.00  cm
    Hole -2: 12.50 cm
    Hole -1: 15.25 cm
    Hole  1: 18.00 cm
    Hole  2: 20.75 cm
    Hole  3: 23.50 cm
    Hole  4: 26.25 cm
    Hole  5: 29.00 cm
    Hole  6: 31.75 cm
    Hole  7: 34.50 cm
    total: 40.5cm
"""

note_mappings = {
    "G3": 196.00,
    "G3#": 207.65,
    "A3": 220.00,
    "A3#": 233.08,
    "B3": 246.94,
    "C4": 261.63,
    "C4#": 277.18,
    "D4": 293.66,
    "D4#": 311.13,
    "E4": 329.63,
    "F4": 349.23,
    "F4#": 369.99,
    "G4": 392.00,
    # "G4#": 415.30,
    # "A4": 440.00,
    # "A4#": 466.16,
    # "B4": 493.88,
    # "C5": 523.25,

   #  "D5": 587.33,
   #  "E5": 659.25,
   #  "F5": 698.46,
   #  "G5": 783.99,
   #  "A5": 880.00,
   #  "B5": 987.77,
}

# Titanic notes
# E  D#  F#  G#  F#  B
# E4 D4# F4# G4# B4/B3

filename_note_mapping = {
    "open":      "G4#",
    "hole_1":    "G4",
    "hole_2":    "F4#",
    "hole_3":    "F4",
    "hole_4":    "E4",
    "hole_5":    "D4#",
    "hole_6":    "D4",
    "hole_7":    "B3",
    "hole_8":    "",

    "Hole_1_G4#": "G4#",
    "Hole_2_G4" : "G4",
    "Hole_3_F4#": "F4#",
    "Hole_4_F4" : "F4",
    "Hole_5_E4_v2" : "E4",
    "Hole_6_D4#": "D4#",
    "Hole_7_D4" : "D4",
    "Hole_8_B3_v2" : "B3",
}

filename_hole_loc_mapping = {
    # "V1": {
    #     "trumpet_-1": 15.25,
    #     "trumpet_2": 20.75,
    #     "trumpet_3": 23.5,
    #     "trumpet_4": 26.25,
    #     "trumpet_5": 29.0,
    #     "trumpet_6": 31.75,
    #     "trumpet_7": 34.5,
    #     "trumpet_all_closed": 40.5,
    # },

    "V2": {
        "V2/Hole_1_G4#": 20.82,
        "V2/Hole_2_G4" : 23.00,
        "V2/Hole_3_F4#": 25.06,
        "V2/Hole_4_F4" : 27.01,
        # "V2/Hole_5_E4" : 28.85,
        "V2/Hole_5_E4_v2" : 28.85,
        "V2/Hole_6_D4#": 30.58,
        "V2/Hole_7_D4" : 32.22,
        # "V2/Hole_8_B3" : 36.60,
        "V2/Hole_8_B3_v2" : 36.60,
    },

    # "V3": {
    #     "V3/open":      16.2,
    #     "V3/hole_1":    18.6,
    #     "V3/hole_2":    20.9,
    #     "V3/hole_3":    23.0,
    #     "V3/hole_4":    25.0,
    #     "V3/hole_5":    26.9,
    #     "V3/hole_6":    28.7,
    #     "V3/hole_7":    33.5,
    #     "V3/hole_8":    40.5,
    # },

    # "V4": {
    #     "V4/open":      16.2,
    #     "V4/hole_1":    18.6,
    #     "V4/hole_2":    20.9,
    #     "V4/hole_3":    23.0,
    #     "V4/hole_4":    25.0,
    #     "V4/hole_5":    26.9,
    #     "V4/hole_6":    28.7,
    #     "V4/hole_7":    33.5,
    #     "V4/hole_8":    39.5,
    # },

    # "V5": {
    #     "V5/open":      16.2,
    #     "V5/hole_1":    18.6,
    #     "V5/hole_2":    20.9,
    #     "V5/hole_3":    23.0,
    #     "V5/hole_4":    25.0,
    #     "V5/hole_5":    26.9,
    #     "V5/hole_6":    28.7,
    #     "V5/hole_7":    33.5,
    #     "V5/hole_8":    40.8,
    # }
}

filenames = [
    # "flute_cover_holes_0",
    # "flute_cover_holes_0_1",
    # "flute_cover_holes_0_1_2",
    # "flute_cover_holes_2",
    # "3_hole_all_open",
    # "3_hole_cover_hole_3",
    # "3_hole_cover_hole_012",
    # "flute_all_open",
    # "final_flute_only_hole_-2",
    # "final_flute_only_hole_-1",
    # "final_flute_only_hole_2",
    # "final_flute_only_hole_3",
    # "final_flute_only_hole_4",
    # "final_flute_only_hole_5",
    # "final_flute_only_hole_6",
    # "final_flute_only_hole_7",

    # "trumpet_holes_after_3",
    # "trumpet_holes_after_4",
    "trumpet_-1",
    "trumpet_2",
    "trumpet_3",
    "trumpet_4",
    "trumpet_5",
    "trumpet_6",
    "trumpet_7",
    "trumpet_all_closed",
]

plt.figure(figsize=(15,10))
# # Plot Frequency spectrum for wav files
# for filename in filenames:
#     fs, data = wavfile.read(filename + ".wav")
#     fft_data = do_fft(data)
#     plt.plot(fft_data, label=filename)

# plt.legend()
# plt.xlabel('Frequency [Hz]')
# plt.ylabel('Fourier values')
# plt.title("Frequency spectrum of Trumpet notes")
# plt.xlim(0, max_freq_show)
# # plt.ylim(0, 5E7)
# plt.show()
# exit()

def fit_func(x, a, b):
    return x * a + b

for version, mapping in filename_hole_loc_mapping.items():
    dists = []
    freqs = []
    for filename, dist in mapping.items():
        fs, data = wavfile.read(filename + ".wav")
        fft_data = do_fft(data)
        #plt.plot(fft_data, label=filename)

        show_freqs = 1
        sorted_freqs = np.argsort(fft_data)
        for i in sorted_freqs[-show_freqs:]:
            # print(filename, i, fft_data[i], sep="\t")
            dists.append(dist)
            freqs.append(i)
            # plt.scatter(dist, i, label=filename)
            # plt.annotate(filename, (dist, i))
            # plt.scatter(dist, i)
            plt.annotate(filename_note_mapping[filename.split('/')[1]], (dist, i))
            closest_note = ""
            closest_diff = 10000
            for note, freq in note_mappings.items():
                diff = abs(freq - i)
                if diff < closest_diff:
                    closest_diff = diff
                    closest_note = note
            print(f"Closest note to {filename} is {closest_note} with an abs diff of {closest_diff}")

        # f, pxx_den = signal.periodogram(data, fs)
        # plt.semilogy(f, pxx_den)
    plt.scatter(dists, freqs, label=version)
    params, conv = optimize.curve_fit(fit_func, dists, freqs)
    print(params)

    fitted_y = []
    for d in dists:
        fitted_y.append(fit_func(d, params[0], params[1]))
    plt.plot(dists, fitted_y, label=f"Fitted")

    # plt.xlabel('Distance of hole from opening [cm]')
    # plt.ylabel('Frequency [Hz]')
    # plt.title(f"Distance of hole vs Frequency {version}")
    # plt.figure(figsize=(15,10))

i = 0
for note, freq in note_mappings.items():
    # plt.hlines(y=freq, xmin=min(dists),  xmax=max(dists), label=note, color=np.random.rand(3,))
    color = colorsys.hsv_to_rgb( i / (len(note_mappings)*2), 1.0, 1.0 )
    plt.hlines(y=freq, xmin=min(dists),  xmax=max(dists), color=color)
    plt.annotate(note, (min(dists)-1, freq))

    # y = mx + b
    # x = (y-b)/m
    dist = (freq - params[1]) / params[0]

    if note in "E4 D4# F4# G4# B3":
        print(f"Note {note} is a hole at {dist} cm")
    # plt.scatter(10, freq, label=note)
    i += 1


# plt.legend()
plt.xlabel('Distance of hole from opening [cm]')
plt.ylabel('Frequency [Hz]')
plt.title("Distance of hole vs Frequency V2")
plt.xlim(min(dists)-1.5, max(dists)+1)
# plt.xlim(0, max_freq_show)
# plt.ylim(0, 5E7)
plt.show()
