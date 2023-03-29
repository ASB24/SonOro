import sys
sys.path.append('./modules')
if True:  # noqa: E402
    import os
    import fileChecker as fc
    import modelTrainer as mt
    import knowledgeEntry as ke
    import helpers as h
    from dotenv import load_dotenv

load_dotenv()

datasetPath = os.getenv('DATASET_PATH')
genresPath = os.getenv('GENRES_PATH')
genresFilePath = os.getenv('GENRES_FILE_PATH')

print('Creating dataset...')
ke.createDataset(datasetPath, genresPath, genresFilePath)
print('Dataset created successfully')

# print('Loading dataset...')
# dataset = fc.loadDataset(datasetPath)
# print('Dataset loaded successfully')

# print('Getting predictions...')
# # get all .mp3 files from a directory and run the model
# filePaths = {}
# for file in os.listdir('./testfiles'):
#     if file.endswith('.mp3'):
#         filePaths[file] = f'./testfiles/{file}'

# for name, path in filePaths.items():
#     filePath = fc.getWavFile(path, convertedFilePath)
#     prediction = mt.getPrediction(filePath, dataset, k, genresPath)
#     print(f'Prediction for {name}: {prediction}')
