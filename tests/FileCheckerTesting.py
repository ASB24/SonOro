from unittest import TestCase

# Chequeo de Archivos
import FileChecker
datasetPath = "assets/dataset.dat"
wavFilePath = "assets/convertedFile.wav"

class TestMethods(TestCase):
    def testFileChecker(self):
        self.assertEqual(FileChecker.getWavFile('./TestFile.mp3', wavFilePath), wavFilePath, "Deberia devolver el path del audio modficado")
        
    def testDatasetLoad(self):
        self.assertIsInstance(FileChecker.loadDataset(datasetPath),list)