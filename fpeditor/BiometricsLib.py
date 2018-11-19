from subprocess import call
from os import path
from PIL import Image


class BiometricsLib:
    LIBRARY_PATH = 'lib/biometrics'
    TMP_FILE = '/tmp/_biometrics.png'

    @staticmethod
    def __biotrics_lib_path():
        bpath = path.dirname(path.dirname(path.abspath(__file__)))
        bpath += '/' + BiometricsLib.LIBRARY_PATH + '/'

        return bpath

    @staticmethod
    def gabor_filter(img, block_size=16):

        img.save(BiometricsLib.TMP_FILE)

        cmd = [
            'python2.7',
            BiometricsLib.__biotrics_lib_path() + 'gabor.py',
            BiometricsLib.TMP_FILE,
            str(block_size),
            BiometricsLib.TMP_FILE
        ]

        call(cmd)
        return Image.open(BiometricsLib.TMP_FILE).convert('RGB')


