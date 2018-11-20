import matplotlib.pyplot as plt
import numpy as np
import scipy.misc as misc
import scipy.ndimage as ndimage
from PIL import Image

from fpeditor.fpie.Utils import Utils
from fpeditor.fpie.WahabUtil import WahabUtil
from fpeditor.fpie.GaborUtil import GaborUtil


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

    @staticmethod
    def find_mask(img):
        img.save(FingerprintIELib.FILE)

        image = ndimage.imread(FingerprintIELib.FILE, mode="L").astype("float64")
        image = Utils.normalize(image)
        mask = Utils.find_mask(image)

        misc.imsave(FingerprintIELib.FILE, mask)
        return Image.open(FingerprintIELib.FILE)

    @staticmethod
    def orientations(img):
        img.save(FingerprintIELib.FILE)

        image = ndimage.imread(FingerprintIELib.FILE, mode="L").astype("float64")
        image = Utils.normalize(image)
        mask = Utils.find_mask(image)

        image = np.where(mask == 1.0, Utils.local_normalize(image), image)
        orientations = np.where(mask == 1.0, Utils.estimate_orientations(image), -1.0)
        Utils.show_orientations(image, orientations, "orientations", 8)

        plt.savefig(FingerprintIELib.FILE, bbox_inches='tight', pad_inches = 0)

        return Image.open(FingerprintIELib.FILE)

    @staticmethod
    def filtering(img, filter_type, subdivide):
        img.save(FingerprintIELib.FILE)

        image = ndimage.imread(FingerprintIELib.FILE, mode="L").astype("float64")
        image = Utils.normalize(image)
        mask = Utils.find_mask(image)

        image = np.where(mask == 1.0, Utils.local_normalize(image), image)
        orientations = np.where(mask == 1.0, Utils.estimate_orientations(image), -1.0)

        frequencies = np.where(mask == 1.0, Utils.estimate_frequencies(image, orientations), -1.0)

        if filter_type == 'gabor':
            if subdivide:
                image = Utils.normalize(GaborUtil.gaborFilterSubdivide(image, orientations, frequencies))
            else:
                image = GaborUtil.gaborFilter(image, orientations, frequencies)
            image = np.where(mask == 1.0, image, 1.0)
        elif filter_type == 'wahab':
            image = np.where(mask == 1.0, WahabUtil.wahab_filter(image, orientations), 1.0)
        else:
            raise SyntaxError('filter type %s is not supported' % filter_type)

        misc.imsave(FingerprintIELib.FILE, image)
        return Image.open(FingerprintIELib.FILE)

