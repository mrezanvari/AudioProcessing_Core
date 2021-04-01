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


recording = '/Users/mrezanvari/_MyFiles/Programs/Python/Spleeter/Spleeter_Trepanation/02 Preparation/other.wav'  # sys.argv[1]
recording2 = '/Users/mrezanvari/_MyFiles/Programs/Python/Spleeter/Spleeter_Trepanation/01 The Key To Conscience/other.wav'
y, sr = librosa.load(recording, sr=None)
y2, sr = librosa.load(recording, sr=None)
checkDir(os.getcwd() + '/Trepanation_out/')
mix = y%y2+y*2
write('Trepanation_out/' + 'out.wav', sr, mix)

