import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import numpy as np
from scipy import signal
from scipy import optimize

# %%

# load the data
# fs, data = wavfile.read('flute_cover_holes_2.wav')
# print("fs", fs, "data len", len(data))
# print("max", max(data), "min", min(data))

max_freq_show = 2000
#%% FFT
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
    "A3": 220.00,
    "B3": 246.94,
    "C4": 261.63,
    "C4#": 277.18,
    "D4": 293.66,
    "D4#": 311.13,
    "E4": 329.63,
    "F4": 349.23,
    "F4#": 369.99,
    "G4": 392.00,
    "G4#": 415.30,
    "A4": 440.00,
    "A4#": 466.16,
    "B4": 493.88,
    "C5": 523.25,
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

filename_hole_loc_mapping = {
        "trumpet_-1": 15.25,
        "trumpet_2": 20.75,
        "trumpet_3": 23.5,
        "trumpet_4": 26.25,
        "trumpet_5": 29.0,
        "trumpet_6": 31.75,
        "trumpet_7": 34.5,
        "trumpet_all_closed": 40.5,
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

def fit_func(x, a, b):
    return x * a + b

dists = []
freqs = []
#for filename in filenames:
for filename, dist in filename_hole_loc_mapping.items():
    fs, data = wavfile.read(filename + ".wav")
    fft_data = do_fft(data)
    #plt.plot(fft_data, label=filename)

    show_freqs = 1
    sorted_freqs = np.argsort(fft_data)
    for i in sorted_freqs[-show_freqs:]:
        # print(filename, i, fft_data[i], sep="\t")
        dists.append(dist)
        freqs.append(i)
        plt.scatter(dist, i, label=filename)
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
params, conv = optimize.curve_fit(fit_func, dists, freqs)
print(params)

fitted_y = []
for d in dists:
    fitted_y.append(fit_func(d, params[0], params[1]))
plt.plot(dists, fitted_y, label="fitted")


for note, freq in note_mappings.items():
    plt.hlines(y=freq, xmin=min(dists),  xmax=max(dists), label=note, color=np.random.rand(3,))

    # y = mx + b
    # x = (y-b)/m
    dist = (freq - params[1]) / params[0]
    
    if note in "E4 D4# F4# G4# B3":
        print(f"Note {note} is a hole at {dist} cm")
    # plt.scatter(10, freq, label=note)


plt.legend()
#plt.xlim(0, max_freq_show)
# plt.ylim(0, 5E7)
plt.show()

# plt.subplot(2, 2, 1)
# plt.plot(abs_freqs,'r')
# plt.xlabel('frequency [Hz]')
# plt.xlim(0, max_freq_show)
# # plt.show()

# #%% welch

# f, pxx = signal.welch(data, fs)
# plt.subplot(2, 2, 2)
# plt.semilogy(f, pxx)
# plt.xlabel('frequency [Hz]')
# plt.ylabel('PSD [V**2/Hz]')
# plt.xlim(0, max_freq_show)
# # plt.show()


# # %%
# plt.subplot(2, 2, 3)
# f, pxx_den = signal.periodogram(data, fs)
# plt.semilogy(f, pxx_den)
# plt.xlabel('frequency [Hz]')
# plt.ylabel('PSD [V**2/Hz]')
# plt.xlim(0, max_freq_show)
# plt.show()


# %%
