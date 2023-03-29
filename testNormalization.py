import sys
sys.path.append('./modules')
if True:
    from pydub import AudioSegment
    import fileChecker as fc
    import os


k = 5
testFilePath = './testfiles/Toxicity.mp3'
convertedFilePath = "./tempFile.wav"
testConvertedAudioPath = "./testConvertedAudio.wav"

# convert to wav if .au exists
filePath = convertedFilePath
if not os.path.isfile(convertedFilePath):
    filePath = fc.getWavFile(testFilePath, convertedFilePath)

audio = AudioSegment.from_file(filePath)
target_loudness = 10
normalized_audio = audio.normalize(target_loudness)
normalized_audio.export(testConvertedAudioPath, format="wav")
