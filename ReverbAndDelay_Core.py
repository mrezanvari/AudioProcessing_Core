import librosa
import librosa.display
import matplotlib.pyplot as plt
import sys
import numpy as np
import os
import glob
import sm as sm
from scipy.io.wavfile import write
from scipy import signal, fftpack
from PIL import Image
import random
from statsmodels.nonparametric.kernel_regression import KernelReg

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

def fadeIn(audio, durationSamples):
        length = int(durationSamples)
        start = 0
        end = start + length
        fade_curve = np.linspace(0.0, 1.0, length)
        audio[start:end] = audio[start:end] * fade_curve


recording = '_Samples/' + 'GUIT.wav'  # sys.argv[1]
y, sr = librosa.load(recording, sr=None)
checkDir(os.getcwd() + '/ReverbDelay_out/')
msDuration = sr/1000


delay = y
delayMS = round(100*msDuration)
delay = np.insert(delay, 0, np.zeros(delayMS))

delay1 = np.insert(delay, 0, np.zeros(round(delayMS*2)))*0.5
delay2 = np.insert(delay1, 0, np.zeros(round(delayMS*4)))*0.6
delay3 = np.insert(delay2, 0, np.zeros(round(delayMS*8)))*0.4
mix = np.zeros(delay3.size)
y.resize(delay3.shape)
delay1.resize(delay3.shape)
delay.resize(delay3.shape)
delay2.resize(delay3.shape)
mix = y + delay + delay1 + delay2 + delay3
write('ReverbDelay_out/' + 'delay.wav', sr, mix)