import sys
import os
sys.path.append('./modules')

import fileChecker as fc
from pydub import AudioSegment

k = 5
testFilePath = './disco.00004.au'
convertedFilePath = "./tempFile.wav"
testConvertedAudioPath = "./testConvertedAudio.wav"

# convert to wav if .au exists
filePath = convertedFilePath
if not os.path.isfile(convertedFilePath):
    filePath = fc.getWavFile(testFilePath, convertedFilePath)

audio = AudioSegment.from_file(filePath)
target_loudness = 15
normalized_audio = audio.normalize(target_loudness)
normalized_audio.export(testConvertedAudioPath, format="wav")