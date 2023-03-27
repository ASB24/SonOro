import os
from pydub import AudioSegment
import pickle
from TrainingModel import extractFeature


def createDataset(datasetPath: str, genresPath: str) -> bool:
    with open(datasetPath, 'wb') as f:
        for folder in os.listdir(genresPath):
            for file in os.listdir(f'{genresPath}/{folder}'):
                try:
                    sound = AudioSegment.from_file(
                        f'{genresPath}/{folder}/{file}')
                    feature = extractFeature(sound)
                    pickle.dump(feature, f)
                except EOFError:
                    f.close()
                except Exception as e:
                    print(e)
                    print(f'Error encountered while parsing file: {file}')
                    f.close()
                    return False
    return True


def loadDataset(datasetPath: str, split: str) -> [List, List]:
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
            trSet.append(dataset[x])
        else:
            teSet.append(dataset[x])

    return trainingsSet, testSet
