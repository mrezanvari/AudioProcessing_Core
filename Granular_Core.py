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

def fadeOut(audio, durationSamples):
    length = int(durationSamples)
    end = audio.shape[0]
    start = end - length
    fade_curve = np.linspace(1.0, 0.0, length)
    audio[start:end] = audio[start:end] * fade_curve
    return audio[start:end], start

def fadeIn(audio, durationSamples):
        length = int(durationSamples)
        start = 0
        end = start + length
        fade_curve = np.linspace(0.0, 1.0, length)
        audio[start:end] = audio[start:end] * fade_curve
        return audio[start:end], end

def blendBetweenMix(audio1, audio2, durationSamples):
    start = audio1.shape[0] - durationSamples
    end = durationSamples
    fadeMix = audio1[start:] + audio2[:end]

    np.delete(audio1, np.arange(start, audio1.shape[0]))
    np.delete(audio2, np.arange(0, end))
    np.insert(audio1, 0, fadeMix[:round(fadeMix.size/2)])
    np.append(audio2, fadeMix[round(fadeMix.size/2):])


def blendBetweenFade(audio1, audio2, durationSamples):
    fade1, start = fadeOut(audio1, durationSamples)
    fade2, end = fadeIn(audio2, durationSamples)
    fadeMix = fade1 + fade2

    np.delete(audio1, np.arange(start, audio1.shape[0]))
    np.delete(audio2, np.arange(0, end))
    np.insert(audio1, 0, fadeMix[:round(fadeMix.size/2)])
    np.append(audio2, fadeMix[round(fadeMix.size/2):])


recording =  '_Samples/' + 'wave.wav'  # sys.argv[1]
y, sr = librosa.load(recording, sr=None)
checkDir(os.getcwd() + '/Granular_out/')

grainCount = 200
granularArray = np.asarray(np.array_split(y, grainCount))
smallestSubArray = granularArray[grainCount-1].size
np.random.shuffle(granularArray)
granularArrayConcat = np.concatenate(granularArray)
write('Granular_out/' + 'outGRAN_Shuffle.wav', sr, granularArrayConcat)

granularArrayFilter = granularArray
for i, grain in enumerate(granularArray):
    fadeOut(grain, round(smallestSubArray*.01))
    fadeIn(grain, round(smallestSubArray*.01))

granularArray = np.concatenate(granularArray)
write('Granular_out/' + 'outGRAN_MyFade.wav', sr, granularArray*.8)

granularArray = np.array_split(y, 1)
granularArray = np.flip(granularArray)
granularArray = np.concatenate(granularArray)
write('Granular_out/' + 'outGRAN_Invert.wav', sr, granularArray)

# granularArray = np.array_split(y, grainCount)
granularArray = np.repeat(y, 2)
# print('Before: ', y)
# print('After: ', granularArray)
# granularArray = np.concatenate(granularArray)
write('Granular_out/' + 'outGRAN_Stretch.wav', sr, granularArray)

granularArray = np.flip(granularArray)
write('Granular_out/' + 'outGRAN_StretchInvert.wav', sr, granularArray)

grainCount = 100 
granularArray = np.asarray(np.array_split(y, grainCount))
smallestSubArray = granularArray[grainCount-1].size
np.random.shuffle(granularArray)
sample = granularArray[0]


for i, grain in enumerate(granularArray):
    if i+1 < grainCount:
        granularArray[i] = sample
        granularArray[i+1] = sample
        # fadeOut(grain, round(smallestSubArray * .1))
        # fadeIn(grain, round(smallestSubArray * .1))
        blendBetweenMix(granularArray[i], granularArray[i+1], round(smallestSubArray * .01))

granularArray = np.concatenate(granularArray)
# plt.figure(1)
# plt.plot(granularArray)
# plt.show()
write('Granular_out/' + 'outGRAN_RandomStretch.wav', sr, granularArray)


exit(0)