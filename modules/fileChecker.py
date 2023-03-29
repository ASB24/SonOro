from os import path
from pydub import AudioSegment
import pickle
from typing import List


def loadDataset(datasetPath: str) -> List:
    try:
        open(datasetPath, "rb").close()
    except FileNotFoundError:
        open(datasetPath, "wb+").close()

    dataset = []
    with open(datasetPath, 'rb') as recordsFile:
        while True:
            try:
                dataset.append(pickle.load(recordsFile))
            except EOFError:
                recordsFile.close()
                break
    return dataset


def getWavFile(filePath: str, wavFilePath: str) -> str:
    try:
        file = open(wavFilePath, "rb+")
        file.truncate()
        file.close()
    except FileNotFoundError:
        file = open(wavFilePath, "w+").close()

    targetLoudness = 15

    audio = AudioSegment.from_file(filePath)

    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(22050)
    audio = audio.normalize(targetLoudness)

    audioExport = audio.export(wavFilePath, format="wav", bitrate="16")
    audioExport.close()

    return wavFilePath
