import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import numpy as np
from scipy import signal

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
    "C5": 523.25,
    "D5": 587.33,
    "E5": 659.25,
    "F5": 698.46,
    "G5": 783.99,
    "A5": 880.00,
    "B5": 987.77,
}

filenames = [
    # "flute_cover_holes_0",
    # "flute_cover_holes_0_1",
    # "flute_cover_holes_0_1_2",
    # "flute_cover_holes_2",
    "3_hole_all_open",
    "3_hole_cover_hole_3",
    "3_hole_cover_hole_012",
    "flute_all_open",
]

for filename in filenames:
    fs, data = wavfile.read(filename + ".wav")
    fft_data = do_fft(data)
    plt.plot(fft_data, label=filename)

    

    show_freqs = 1
    sorted_freqs = np.argsort(fft_data)
    for i in sorted_freqs[-show_freqs:]:
        print(filename, i, fft_data[i], sep="\t")

plt.legend()
plt.xlim(0, max_freq_show)
plt.ylim(0, 5E7)
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
