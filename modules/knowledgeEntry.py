import os
import random
from typing import List
from pydub import AudioSegment
import pickle
from helpers import extractFeature


def createDataset(datasetPath: str, genresPath: str) -> bool:
    if os.path.exists(datasetPath):
        os.remove(datasetPath)
        
    with open(datasetPath, 'wb') as f:
        i = 0
        path = ''
        for folder in os.listdir(genresPath):
            i += 1
            print(folder)
            for file in os.listdir(f'{genresPath}/{folder}'):
                try:
                    path = f'{genresPath}/{folder}/{file}'
                    if not file.endswith(".wav"):
                        path = convertToWav(path)
                    
                    audio = AudioSegment.from_file(path)

                    target_loudness = 15
                    normalized_audio = audio.normalize(target_loudness)
                    normalized_audio.export(path, format="wav")
                        
                    feature = extractFeature(path, i)
                    
                    pickle.dump(feature, f)
                    
                except EOFError:
                    f.close()
                except Exception as e:
                    print(e)
                    print(f'Error encountered while parsing file: {file}')
                    f.close()
                    return False
    return True

def convertToWav(filePath: str) -> str:
    sound = AudioSegment.from_file(filePath)
    
    os.remove(filePath)
    
    path = '.'.join(filePath.split('.')[:-1])
    wavPath = f'{path}.wav'
    
    sound = sound.export(wavPath, format='wav')
    sound = AudioSegment.from_file(wavPath)
    return wavPath

def loadDatasets(datasetPath: str, split: float) -> List:
    dataset = []
    trainingsSet = []
    testSet = []

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

    for x in range(len(dataset)):
        if random.random() < split:
            trainingsSet.append(dataset[x])
        else:
            testSet.append(dataset[x])

    return trainingsSet, testSet
