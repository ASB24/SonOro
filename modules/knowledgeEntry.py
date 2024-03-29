import os
import random
from typing import List
from pydub import AudioSegment
import pickle
from helpers import extractFeature
from collections import defaultdict
from multiprocessing import Pool
import time


def createDataset(datasetPath: str, genresPath: str, genresFilePath: str) -> bool:
    if os.path.exists(datasetPath):
        os.remove(datasetPath)
    if os.path.exists(genresFilePath):
        os.remove(genresFilePath)

    genres = defaultdict(int)
    threadDatasets = []

    numThreads = os.cpu_count()-2

    start = time.time()
    with Pool(numThreads) as pool:
        for i, folder in enumerate(os.listdir(genresPath)):
            i += 1
            genres[i] = folder
            threadDatasetPath = f'temp/thread_{i}.dat'
            threadDatasets.append(threadDatasetPath)
            pool.apply_async(processFolder,
                             (genresPath, folder, threadDatasetPath, i))

        pool.close()
        pool.join()
    print(f'Elapsed time: {time.time() - start} seconds')

    with open(datasetPath, 'wb') as datasetFile:
        for threadDatasetPath in threadDatasets:
            with open(threadDatasetPath, 'rb') as threadDataset:
                datasetFile.write(threadDataset.read())
            os.remove(threadDatasetPath)

    print('Writing genres to file...')
    with open(genresFilePath, 'wb') as genresFile:
        pickle.dump(genres, genresFile)

    return True


def processFolder(genresPath, folder, threadDatasetPath, genreIndex):
    print(f'Processing {folder}...')
    with open(threadDatasetPath, 'wb') as datasetFile:
        path = ''
        for file in os.listdir(f'{genresPath}/{folder}'):
            try:
                path = f'{genresPath}/{folder}/{file}'

                if not file.endswith(".wav"):
                    path = convertToWav(path)

                feature = extractFeature(path, genreIndex)
                pickle.dump(feature, datasetFile)

            except Exception as e:
                print(e)
                print(f'Error encountered while parsing file: {file}')
                datasetFile.close()
                return False

    return True
# def createDataset(datasetPath: str, genresPath: str, genresFilePath: str) -> bool:
#     if os.path.exists(datasetPath):
#         os.remove(datasetPath)
#     if os.path.exists(genresFilePath):
#         os.remove(genresFilePath)

#     genres = defaultdict(int)

#     with open(datasetPath, 'wb') as datasetFile:
#         i = 0
#         path = ''
#         for folder in os.listdir(genresPath):
#             i += 1
#             genres[i] = folder
#             print(f'Processing {genres[i]}...')
#             for file in os.listdir(f'{genresPath}/{folder}'):
#                 try:
#                     path = f'{genresPath}/{folder}/{file}'

#                     if not file.endswith(".wav"):
#                         path = convertToWav(path)

#                     audio = AudioSegment.from_file(path)

#                     target_loudness = 10
#                     normalized_audio = audio.normalize(target_loudness)
#                     normalized_audio.export(path, format="wav")
#                     try:
#                         insertToDataset(datasetFile, path, i)
#                     except Exception as e:
#                         print(e)
#                         datasetFile.close()

#                 except EOFError:
#                     datasetFile.close()
#                 except Exception as e:
#                     print(e)
#                     print(f'Error encountered while parsing file: {file}')
#                     datasetFile.close()
#                     return False

#     print('Writing genres to file...')
#     with open(genresFilePath, 'wb') as genresFile:
#         pickle.dump(genres, genresFile)

#     return True


def insertToDataset(datasetFile: str, filePath: str, iterations: int) -> bool:
    if isinstance(datasetFile, str):
        datasetFile = open(datasetFile, 'ab')

    try:
        feature = extractFeature(filePath, iterations)
        pickle.dump(feature, datasetFile)
    except EOFError:
        datasetFile.close()
        return False
    except Exception as e:
        print(e)
        datasetFile.close()
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
