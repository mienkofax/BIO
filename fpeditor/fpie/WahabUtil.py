import numpy as np
from skimage import draw

from fpeditor.fpie.Utils import Utils


class WahabUtil:
    @staticmethod
    def wahab_kernel(size, angle):
        y = int(np.sin(angle) * size)
        x = int(np.cos(angle) * size)

        kernel = np.zeros((np.abs(y) + 1, np.abs(x) + 1))

        if y < 0:
            rr, cc = draw.line(0, 0, y, x)
        else:
            rr, cc = draw.line(-y, 0, 0, x)

        kernel[rr, cc] = 1.0
        return kernel

    @staticmethod
    def wahab_filter(image, orientations, w=8):
        result = np.empty(image.shape)

        height, width = image.shape
        for y in range(0, height - w, w):
            for x in range(0, width - w, w):
                orientation = orientations[y+w//2, x+w//2]
                kernel = WahabUtil.wahab_kernel(16, orientation)
                result[y:y+w, x:x+w] = Utils.convolve(image, kernel, (y, x), (w, w))
                result[y:y+w, x:x+w] /= np.sum(kernel)

        return result
