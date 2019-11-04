#!/usr/bin/python
# based on : www.daniweb.com/code/snippet263775.html
import math
import wave
import struct

# Audio will contain a long list of samples (i.e. floating point numbers describing the
# waveform).  If you were working with a very long sound you'd want to stream this to
# disk instead of buffering it all in memory list this.  But most sounds will fit in
# memory.
sample_rate = 44100.0


def generate_silence(duration_milliseconds=500):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    audio = []
    for x in range(int(num_samples)):
        audio.append(0.0)

    return audio


def generate_sinewave(
        freq=440.0,
        duration_milliseconds=500,
        volume=1.0):
    """
    The sine wave generated here is the standard beep.  If you want something
    more aggressive you could try a square or saw tooth waveform.   Though there
    are some rather complicated issues with making high quality square and
    sawtooth waves... which we won't address here :)
    """

    audio = []

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        audio.append(volume * math.sin(2 * math.pi * freq * ( x / sample_rate )))

    return audio


def save_wav(file_name, audio):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")

    # wav params
    nchannels = 1

    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theoretically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

    return

freqs = [
    # 350,
    # 440,
    # 480,
    697,
    # 1046.50,
    1477,
]
audio = []
for freq in freqs:
    new_audio = generate_sinewave(freq=freq, duration_milliseconds=2000)
    if not audio:
        audio = new_audio
    else:
        for i in range(len(audio)):
            audio[i] += new_audio[i]

for i in range(len(audio)):
    audio[i] /= len(freqs)

# p440 = generate_sinewave(duration_milliseconds=1000)
# p1000 = generate_sinewave(freq=1046.50, duration_milliseconds=1000)

# audio = [(p440[i] + p1000[i])/2 for i in range(len(p440))]
save_wav("output.wav", audio)
