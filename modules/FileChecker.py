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

    audio = AudioSegment.from_file(filePath)
    audioExport = audio.export(wavFilePath, format="wav")
    audioExport.close()

    return wavFilePath
