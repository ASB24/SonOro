from unittest import TestCase

# Chequeo de Archivos
import FileChecker
import pathlib as pl

datasetPath = "assets/dataset.dat"
wavFilePath = "assets/tempFile.wav"

class TestMethods(TestCase):
    def testFileChecker(self):
        resultFilePath = FileChecker.getWavFile('./TestFile.mp3', wavFilePath)
        if not pl.Path(wavFilePath).is_file():
            self.fail("El archivo no existe")
        self.assertEqual(resultFilePath, wavFilePath, "Deberia devolver el path del audio modficado")
        self.assertIsInstance(resultFilePath, str, "El resultado deberia ser un string")
        
    def testDatasetLoad(self):
        self.assertIsInstance(FileChecker.loadDataset(datasetPath),list)