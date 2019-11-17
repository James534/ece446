# %%
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
    show_freqs = 5
    sorted_freqs = np.argsort(abs_freqs)
    for i in sorted_freqs[-show_freqs:]:
        print(i, abs_freqs[i])
    return abs_freqs

filenames = [
    "flute_cover_holes_0",
    # "flute_cover_holes_0_1",
    # "flute_cover_holes_0_1_2",
    # "flute_cover_holes_2",
]

for filename in filenames:
    fs, data = wavfile.read(filename + ".wav")
    fft_data = do_fft(data)
    plt.plot(fft_data, label=filename)

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
