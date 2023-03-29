from unittest import TestCase

# Chequeo de Archivos
import fileChecker
import pathlib as pl

datasetPath = "assets/dataset.dat"
wavFilePath = "assets/tempFile.wav"
testFilePath = './TestFile.mp3'

class TestMethods(TestCase):
    def testFileChecker(self):
        resultFilePath = fileChecker.getWavFile(testFilePath, wavFilePath)
        if not pl.Path(wavFilePath).is_file():
            self.fail("El archivo no existe")
        self.assertEqual(resultFilePath, wavFilePath, "Deberia devolver el path del audio modficado")
        self.assertIsInstance(resultFilePath, str, "El resultado deberia ser un string")