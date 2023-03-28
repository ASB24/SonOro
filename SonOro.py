import os
import sys
sys.path.append('./modules')

import fileChecker as fc
import modelTrainer as mt
import knowledgeEntry as ke
import helpers as h

k = 5
testFilePath = './TestFile.mp3'
datasetPath = "assets/dataset.dat"
convertedFilePath = "assets/tempFile.wav"
genresPath = "assets/genres"

print('Creating dataset...')
ke.createDataset(datasetPath, genresPath)
print('Dataset created successfully')

print('Loading dataset...')
dataset = fc.loadDataset(datasetPath)
print('Dataset loaded successfully')

print('Getting predictions...')
#get all .mp3 files from a directory and run the model
filePaths = {}
for file in os.listdir('./testfiles'):
    if file.endswith('.mp3'):
        filePaths[file] = f'./testfiles/{file}'
    
for name, path in filePaths.items():
    filePath = fc.getWavFile(path, convertedFilePath)
    prediction = mt.getPrediction(filePath, dataset, k, genresPath)
    print(f'Prediction for {name}: {prediction}')
    



