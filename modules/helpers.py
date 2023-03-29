from collections import defaultdict
import os
import numpy as np
from scipy.io import wavfile as wav
from python_speech_features import mfcc
import pickle


def extractFeature(soundFile, iterations):
    (rate, sig) = wav.read(soundFile)
    mfccFeat = mfcc(sig, rate, winlen=0.2, nfft=8820, appendEnergy=False)
    covariance = np.cov(np.matrix.transpose(mfccFeat))
    meanMatrix = mfccFeat.mean(0)
    feature = (meanMatrix, covariance, iterations)

    return feature


def getGenres(genresFilePath):
    genres = defaultdict(int)

    with open(genresFilePath, 'rb') as genresFile:
        genres = pickle.load(genresFile)

    return genres
