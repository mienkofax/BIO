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

    @staticmethod
    def skeletonization_filter(img):

        img.save(BiometricsLib.TMP_FILE)

        cmd = [
            'python2.7',
            BiometricsLib.__biotrics_lib_path() + 'thining.py',
            BiometricsLib.TMP_FILE,
            BiometricsLib.TMP_FILE
        ]

        call(cmd)
        return Image.open(BiometricsLib.TMP_FILE).convert('RGB')

    @staticmethod
    def singular_points(img, block_size=16, tolerance=1, enable_smooth=True):

        img.save(BiometricsLib.TMP_FILE)

        smooth = ''
        if enable_smooth:
            smooth = '--smooth'

        cmd = [
            'python2.7',
            BiometricsLib.__biotrics_lib_path() + 'poincare.py',
            BiometricsLib.TMP_FILE,
            str(block_size),
            str(tolerance),
            str(smooth),
            BiometricsLib.TMP_FILE
        ]

        call(cmd)
        return Image.open(BiometricsLib.TMP_FILE).convert('RGB')

    @staticmethod
    def ridge_filter(img):

        img.save(BiometricsLib.TMP_FILE)

        cmd = [
            'python2.7',
            BiometricsLib.__biotrics_lib_path() + 'crossing_number.py',
            BiometricsLib.TMP_FILE,
            BiometricsLib.TMP_FILE
        ]

        call(cmd)
        return Image.open(BiometricsLib.TMP_FILE).convert('RGB')


