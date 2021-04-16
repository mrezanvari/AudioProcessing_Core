import librosa
import librosa.display
import matplotlib.pyplot as plt
import sys
import numpy as np
import os
import glob
from scipy.io.wavfile import write
from scipy import signal, fftpack
from PIL import Image
import random

def checkDir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

outFilePath = os.path.expanduser("~/Desktop/")
recording = '_Samples/' + 'AudioSample3_CLEAN.wav'  # sys.argv[1]
# recording2 = 'AudioSample.mp3' #sys.argv[1]

y, sr = librosa.load(recording, sr=None)
# y2, sr = librosa.load(recording2, sr=None)
checkDir(os.getcwd() + '/Vocoder_out/')

# Frequency / pitch of the sine wave
freq_hz = 660

shift = -2
each_sample_number = np.arange(y.size)
waveformSQR = signal.square(2 * np.pi * each_sample_number * freq_hz / sr)
waveformSIN = np.sin(2 * np.pi * each_sample_number * freq_hz / sr)
waveformSAW = signal.sawtooth(2 * np.pi * each_sample_number * freq_hz / sr)
waveformTAN = np.tan(2 * np.pi * each_sample_number * freq_hz / sr)
waveformNOIZ = np.random.normal(2 * np.pi * each_sample_number * freq_hz / sr)
# np.random.shuffle(waveformSIN)
waveformMIX = waveformSIN

waveform = waveformMIX

waveform *= .3
waveform = np.int16(waveform * 32767)

write('Vocoder_out/' + 'wave.wav', sr, waveform)
vocoderWet = np.multiply(y, waveform) / 4000
write('Vocoder_out/' + 'out1.wav', sr, vocoderWet)

mixConst = .8
vocoderMix = vocoderWet * mixConst
write('Vocoder_out/' + 'out2.wav', sr, np.multiply(vocoderMix, y) * 2)
newMix = np.add(y, vocoderMix) * 10
write('Vocoder_out/' + 'out3.wav', sr, np.add(y, vocoderMix))

# write('Vocoder_out/' + 'outMIX.wav', sr, y*np.resize(y2,y.size))
#
# print(newMix)
# for i, sample in enumerate(newMix):
#     newMix[i] = sample-random.uniform(0,-1)
#
# print(newMix)
# write('Vocoder_out/' + 'out4.wav', sr, newMix)

exit(0)
