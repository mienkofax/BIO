import scipy.misc as misc
import scipy.ndimage as ndimage
from PIL import Image

from fpeditor.fpie.Utils import Utils


class FingerprintIELib:
    """Fingerprint image enhancement"""
    FILE = '/tmp/custom.png'

    @staticmethod
    def normalize(img):
        img.save(FingerprintIELib.FILE)

        image = ndimage.imread(FingerprintIELib.FILE, mode="L").astype("float64")
        image = Utils.normalize(image)

        misc.imsave(FingerprintIELib.FILE, image)
        return Image.open(FingerprintIELib.FILE)
