from os import path
from pydub import AudioSegment
import pickle
from typing import List
from tempfile import NamedTemporaryFile


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


def getWavFile(filePath, wavFilePath: str) -> str:
    if isinstance(filePath, bytes):
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(filePath)
            temp_file.flush()
            temp_file.close()
            filePath = temp_file.name
    elif isinstance(filePath, str):
        pass
    else:
        raise ValueError('Invalid input type. Expected bytes or str.')

    try:
        file = open(wavFilePath, "rb+")
        file.truncate()
        file.close()
    except FileNotFoundError:
        file = open(wavFilePath, "w+").close()
    except pydub.exceptions.CouldntDecodeError:
        raise Exception('The file is not a valid audio file.')

    targetLoudness = 15

    audio = AudioSegment.from_file(filePath)

    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(22050)
    audio = audio.normalize(targetLoudness)

    audioExport = audio.export(
        wavFilePath, format="wav", bitrate="16")
    audioExport.close()

    return wavFilePath
