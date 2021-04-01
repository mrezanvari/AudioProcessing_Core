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


outFilePath = os.path.expanduser("~/Desktop/")
recording = '_Samples/' + 'AudioSample8.wav'  # sys.argv[1]
# recording2 = 'AudioSample.mp3' #sys.argv[1]
# imgData = np.array(Image.open('img.jpg'))

y, sr = librosa.load(recording, sr=None)
# y2, sr = librosa.load(recording2, sr=None)

checkDir(os.getcwd() + '/Filters_out/')